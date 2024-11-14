from typing import Dict, Any
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


class AuthBase:
    async def get_headers(self) -> Dict[str, str]:
        """Retrieve headers for authentication."""
        raise NotImplementedError("Must implement get_headers in subclass.")

    async def get_token_info(self) -> Dict[str, Any]:
        """Retrieve metadata about the current token."""
        raise NotImplementedError("Must implement get_token_info in subclass.")

    async def _request(
        self, method: str, url: str, headers=None, **kwargs
    ) -> Dict[str, Any]:
        """Helper method to manage HTTP requests with error handling."""

        # Correct common protocol typos and enforce https:// if needed
        if not url.startswith("https://"):
            # Check for common protocol typos and strip unsupported protocols
            corrected_url = re.sub(
                r"^\w+://", "", url
            )  # Remove existing protocol if invalid
            logging.debug(
                f"Correcting protocol for URL '{url}' to 'https://{corrected_url}'"
            )
            url = f"https://{corrected_url}"
        try:
            async with httpx.AsyncClient() as client:
                logging.debug(f"URL '{url}'")
                response = await client.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()  # Raise an error for HTTP statuses

            # Log response details for debugging
            logging.debug(f"URL: {url}")
            logging.debug(f"Method: {method}")
            logging.debug(f"Response Status Code: {response.status_code}")
            logging.debug(f"Response Headers: {response.headers}")
            logging.debug(f"Response Content: {response.content}")

            # Check Content-Type to decide how to handle response
            if response.headers.get("Content-Type") == "application/json":
                return response.json()
            elif response.content:
                return {"text": response.text}  # Return raw text if not JSON
            else:
                return {}  # Return empty dict if there's no content

        except httpx.HTTPStatusError as exc:
            # Handle Netsapiens-specific error messages
            try:
                if exc.response.headers.get("Content-Type") == "application/json":
                    error_data = exc.response.json()
                    code = error_data.get("code", exc.response.status_code)
                    message = error_data.get("message", exc.response.text)
                else:
                    # If error response is not JSON, use raw text
                    code = exc.response.status_code
                    message = exc.response.text
            except ValueError:
                # Fallback for unexpected parsing errors
                code = exc.response.status_code
                message = exc.response.text

            # Raise appropriate custom error based on status code
            if exc.response.status_code == 400:
                raise BadRequestError(code=code, message=message) from exc
            elif exc.response.status_code == 401:
                raise AuthenticationError(code=code, message=message) from exc
            elif exc.response.status_code == 403:
                raise ForbiddenError(code=code, message=message) from exc
            elif exc.response.status_code == 404:
                raise NotFoundError(code=code, message=message) from exc
            else:
                # For other HTTP errors, raise a general API error
                raise NetsapiensAPIError(code=code, message=message) from exc


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
