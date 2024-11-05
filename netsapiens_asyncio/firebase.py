from typing import Dict, Any
from .auth import AuthBase


class FirebaseManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the FirebaseManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def read_firebase_service_accounts(self) -> Dict[str, Any]:
        """Retrieve all Firebase service accounts. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_firebase_service_accounts() is not yet implemented."
        )

    async def add_firebase_service_account(
        self, account_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a new Firebase service account with the provided data. Placeholder until implemented."""
        raise NotImplementedError(
            "The method add_firebase_service_account() is not yet implemented."
        )
