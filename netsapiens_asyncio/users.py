from typing import Dict, Any
from .auth import AuthBase


class UserManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the UserManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def search_users_in_domain(
        self, domain: str, query: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Search for users in a domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method search_users_in_domain() is not yet implemented."
        )

    async def create_user_in_domain(
        self, domain: str, user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a user in a domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method create_user_in_domain() is not yet implemented."
        )

    async def count_users_in_domain(self, domain: str) -> Dict[str, Any]:
        """Count users in a domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method count_users_in_domain() is not yet implemented."
        )

    async def delete_user_in_domain(self, domain: str, user_id: str) -> Dict[str, Any]:
        """Delete a user in a domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method delete_user_in_domain() is not yet implemented."
        )

    async def update_user_in_domain(
        self, domain: str, user_id: str, user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a user in a domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_user_in_domain() is not yet implemented."
        )

    async def get_specific_user_in_domain(
        self, domain: str, user_id: str
    ) -> Dict[str, Any]:
        """Retrieve a specific user in a domain by ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_specific_user_in_domain() is not yet implemented."
        )

    async def get_my_user(self) -> Dict[str, Any]:
        """Retrieve information about the authenticated user. Placeholder until implemented."""
        raise NotImplementedError("The method get_my_user() is not yet implemented.")
