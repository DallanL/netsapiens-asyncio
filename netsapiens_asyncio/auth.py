from typing import Optional
from abc import ABC, abstractmethod
import httpx
from datetime import datetime, timedelta, timezone
import jwt


class AuthBase(ABC):
    @abstractmethod
    async def get_headers(self) -> dict:
        """Method to retrieve headers for authentication."""
        pass


class ApiKeyAuth(AuthBase):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.api_key}", "accept": "application/json"}


class OAuth2Auth(AuthBase):
    def __init__(self, client_id: str, client_secret: str, token_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.access_token = None
        self.token_expires_at = None

    async def _fetch_token(self):
        """Fetches a new OAuth2 token."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3600)
            self.token_expires_at = datetime.now(timezone.utc) + timedelta(
                seconds=expires_in
            )

    async def get_headers(self) -> dict:
        """Retrieve headers with a fresh token if needed."""
        if not self.access_token or (
            self.token_expires_at
            and datetime.now(timezone.utc) >= self.token_expires_at
        ):
            await self._fetch_token()
        return {
            "Authorization": f"Bearer {self.access_token}",
            "accept": "application/json",
        }


class JWTAuth(AuthBase):
    def __init__(
        self,
        jwt_token: Optional[str] = None,
        secret_key: Optional[str] = None,
        algorithm: str = "HS256",
    ):
        self.jwt_token = jwt_token
        self.secret_key = secret_key
        self.algorithm = algorithm

    def generate_token(self, payload: dict):
        """Generate a new JWT token."""
        if not self.secret_key:
            raise ValueError("Secret key is required to generate a JWT")
        self.jwt_token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    async def get_headers(self) -> dict:
        """Retrieve headers with the JWT token."""
        if not self.jwt_token:
            raise ValueError("JWT token is required for authorization")
        return {
            "Authorization": f"Bearer {self.jwt_token}",
            "accept": "application/json",
        }
