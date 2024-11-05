from typing import Dict, Any
from .auth import AuthBase


class ResellerManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the ResellerManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def get_resellers(self) -> Dict[str, Any]:
        """Retrieve all resellers. Placeholder until implemented."""
        raise NotImplementedError("The method get_resellers() is not yet implemented.")

    async def create_reseller(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new reseller. Placeholder until implemented."""
        raise NotImplementedError(
            "The method create_reseller() is not yet implemented."
        )

    async def update_reseller(
        self, reseller_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing reseller. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_reseller() is not yet implemented."
        )

    async def delete_reseller(self, reseller_id: str) -> Dict[str, Any]:
        """Delete a reseller by ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method delete_reseller() is not yet implemented."
        )

    async def get_specific_reseller(self, reseller_id: str) -> Dict[str, Any]:
        """Retrieve a specific reseller by ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_specific_reseller() is not yet implemented."
        )
