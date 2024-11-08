from typing import Dict, Any
import httpx
from datetime import datetime, timezone, timedelta
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

    async def _request(self, method: str, url: str, headers=None, **kwargs):
        """Helper method to manage HTTP requests with error handling."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()  # Raise for HTTP error statuses

            return response.json()

        except httpx.HTTPStatusError as exc:
            # Handle Netsapiens-specific error messages
            error_data = exc.response.json()
            code = error_data.get("code", exc.response.status_code)
            message = error_data.get("message", exc.response.text)

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

    async def _fetch_token(self):
        """Fetch a new OAuth2 token using the resource owner credentials grant."""
        token_url = self.primary_token_url
        try:
            response = await self._request_token(token_url)
        except NetsapiensAPIError as e:
            # Check if response appears to be HTML, indicating a fallback is needed
            if "<html" in e.message.lower():
                # Retry with fallback URL if primary URL response suggests an HTML error page
                token_url = self.fallback_token_url
                response = await self._request_token(token_url)
            else:
                raise e

        # Extract token details from response
        self.access_token = response["access_token"]
        expires_in = response.get("expires_in", 3600)
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
        """Retrieve OAuth2 token metadata."""
        return {
            "access_token": self.access_token,
            "expires_at": self.token_expires_at,
            "client_id": self.client_id,
            "username": self.username,
        }
