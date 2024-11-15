from typing import Dict, Any
from abc import ABC, abstractmethod
import httpx
from datetime import datetime, timezone, timedelta
import logging
import re
from .exceptions import (
    BadRequestError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    NetsapiensAPIError,
)

logger = logging.getLogger(__name__)


class AuthBase(ABC):
    @abstractmethod
    async def get_headers(self) -> Dict[str, str]:
        """Retrieve headers for authentication."""
        raise NotImplementedError("Must implement get_headers in subclass.")

    @abstractmethod
    async def get_token_info(self) -> Dict[str, Any]:
        """Retrieve metadata about the current token."""
        raise NotImplementedError("Must implement get_token_info in subclass.")

    async def _request(
        self, method: str, url: str, headers=None, **kwargs
    ) -> Dict[str, Any]:
        """Helper method to manage HTTP requests with error handling and detailed logging."""

        # Log entry to the method
        logger.debug("Entering AuthBase._request")
        logger.debug(f"HTTP Method: {method}")
        logger.debug(f"Initial URL: {url}")
        logger.debug(f"Headers: {headers}")
        logger.debug(f"Additional kwargs: {kwargs}")

        # Correct the URL if protocol is missing or incorrect
        if not url.startswith("https://"):
            corrected_url = re.sub(
                r"^\w+://", "", url
            )  # Remove existing protocol if invalid
            url = f"https://{corrected_url}"
            logger.debug(f"Corrected URL to: {url}")

        try:
            # Log the final URL and request details
            async with httpx.AsyncClient() as client:
                logger.debug(f"Sending request to URL: {url}")
                response = await client.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()  # Raise for HTTP error statuses

            # Log response details
            logger.debug("Request succeeded")
            logger.debug(f"Response Status Code: {response.status_code}")
            logger.debug(f"Response Headers: {response.headers}")
            logger.debug(f"Response Content: {response.content}")

            # Check and parse the response based on Content-Type
            if response.headers.get("Content-Type") == "application/json":
                json_response = response.json()
                logger.debug(f"JSON Response: {json_response}")
                return json_response
            elif response.content:
                text_response = response.text
                logger.debug(f"Text Response: {text_response}")
                return {"text": text_response}
            else:
                logger.debug("Empty response received")
                return {}

        except httpx.HTTPStatusError as exc:
            # Log HTTP error details
            logger.error(f"HTTPStatusError occurred: {exc.response.status_code}")
            logger.error(f"Response content: {exc.response.content}")

            # Parse and log error content if available
            try:
                if exc.response.headers.get("Content-Type") == "application/json":
                    error_data = exc.response.json()
                    code = error_data.get("code", exc.response.status_code)
                    message = error_data.get("message", exc.response.text)
                else:
                    code = exc.response.status_code
                    message = exc.response.text
            except ValueError:
                code = exc.response.status_code
                message = exc.response.text

            logger.error(f"Error Code: {code}, Message: {message}")

            # Raise appropriate custom errors based on status code
            if exc.response.status_code == 400:
                raise BadRequestError(code=code, message=message) from exc
            elif exc.response.status_code == 401:
                raise AuthenticationError(code=code, message=message) from exc
            elif exc.response.status_code == 403:
                raise ForbiddenError(code=code, message=message) from exc
            elif exc.response.status_code == 404:
                raise NotFoundError(code=code, message=message) from exc
            else:
                raise NetsapiensAPIError(code=code, message=message) from exc
        finally:
            # Log exit from the method
            logger.debug("Exiting AuthBase._request")


class ApiKeyAuth(AuthBase):
    def __init__(self, api_key: str, server_url: str):
        self.api_key = api_key
        self.server_url = server_url

    async def get_headers(self) -> Dict[str, str]:
        """Return headers containing the API key."""
        return {"Authorization": f"Bearer {self.api_key}", "accept": "application/json"}

    async def get_token_info(self) -> Dict[str, Any]:
        """Retrieve API key metadata by making a request to the API."""
        url = f"https://{self.server_url}/ns-api/v2/apikeys/~"
        headers = await self.get_headers()
        return await self._request("GET", url, headers=headers)


class JWTAuth(AuthBase):
    def __init__(
        self,
        server_url: str,
        client_id: str,
        username: str,
        password: str,
        client_secret: str,
    ):
        self.server_url = server_url
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = None

    async def _fetch_token(self):
        """Fetch a new JWT token."""
        url = f"https://{self.server_url}/ns-api/v2/jwt"
        response = await self._request(
            "POST",
            url,
            headers={"content-type": "application/json", "accept": "application/json"},
            json={
                "grant_type": "password",
                "client_id": self.client_id,
                "username": self.username,
                "password": self.password,
                "client_secret": self.client_secret,
            },
        )
        self.access_token = response["token"]
        self.token_expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=60
        )  # Set token expiry based on API info

    async def _refresh_token(self):
        """Refresh the JWT token."""
        url = f"https://{self.server_url}/ns-api/v2/jwt"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "accept": "application/json",
        }
        response = await self._request(
            "POST", url, headers=headers, json={"grant_type": "refresh_token"}
        )
        self.access_token = response["token"]
        self.token_expires_at = datetime.now(timezone.utc) + timedelta(minutes=60)

    async def get_headers(self) -> Dict[str, str]:
        """Retrieve headers with a valid JWT token, refreshing if needed."""
        if not self.access_token or (
            self.token_expires_at
            and datetime.now(timezone.utc) >= self.token_expires_at
        ):
            await self._fetch_token()
        return {
            "Authorization": f"Bearer {self.access_token}",
            "accept": "application/json",
        }

    async def get_token_info(self) -> Dict[str, Any]:
        """Retrieve JWT token metadata."""
        url = f"https://{self.server_url}/ns-api/v2/jwt"
        headers = await self.get_headers()
        return await self._request("GET", url, headers=headers)


class OAuth2Auth(AuthBase):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        username: str,
        password: str,
        server_url: str,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.server_url = server_url
        self.access_token = None
        self.token_expires_at = None
        self.primary_token_url = f"https://{self.server_url}/ns-api/v2/tokens"
        self.fallback_token_url = f"https://{self.server_url}/ns-api/oauth2/token/"
        self.token_data = {}  # Store token data and metadata here

    async def _fetch_token(self):
        """Fetch a new OAuth2 token using the resource owner credentials grant."""
        token_url = self.primary_token_url
        try:
            response = await self._request_token(token_url)
            self.token_data = response  # Store token response data
            self.token_data["apiv1"] = False  # Indicate V2 API was used
        except NetsapiensAPIError as e:
            # Check if response appears to be HTML, indicating a fallback is needed
            if "<html" in e.message.lower():
                # Retry with fallback URL if primary URL response suggests an HTML error page
                token_url = self.fallback_token_url
                response = await self._request_token(token_url)
                self.token_data = response  # Store token response data
                self.token_data["apiv1"] = True  # Indicate V1 API was used
            else:
                raise e

        # Extract token details
        self.access_token = self.token_data["access_token"]
        expires_in = self.token_data.get("expires_in", 3600)
        self.token_expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=expires_in
        )

    async def _request_token(self, url: str) -> Dict[str, Any]:
        """Helper function to request a token from a given URL."""
        return await self._request(
            "POST",
            url,
            headers={"content-type": "application/json", "accept": "application/json"},
            json={
                "grant_type": "password",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "username": self.username,
                "password": self.password,
            },
        )

    async def get_headers(self) -> Dict[str, str]:
        """Retrieve headers with a valid OAuth2 token, refreshing if needed."""
        if not self.access_token or (
            self.token_expires_at
            and datetime.now(timezone.utc) >= self.token_expires_at
        ):
            await self._fetch_token()
        return {
            "Authorization": f"Bearer {self.access_token}",
            "accept": "application/json",
        }

    async def get_token_info(self) -> Dict[str, Any]:
        """Return the token data and metadata."""
        return self.token_data
