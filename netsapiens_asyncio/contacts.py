from typing import Dict, Any
from .auth import AuthBase


class ContactManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the ContactManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def get_contacts_for_user(self, user_id: str) -> Dict[str, Any]:
        """Retrieve all contacts for a specific user. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_contacts_for_user() is not yet implemented."
        )

    async def create_contact(
        self, user_id: str, contact_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new contact for a user. Placeholder until implemented."""
        raise NotImplementedError("The method create_contact() is not yet implemented.")

    async def get_specific_contact_for_user(
        self, user_id: str, contact_id: str
    ) -> Dict[str, Any]:
        """Retrieve a specific contact for a user by contact ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_specific_contact_for_user() is not yet implemented."
        )

    async def update_contact(
        self, user_id: str, contact_id: str, contact_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific contact for a user by contact ID. Placeholder until implemented."""
        raise NotImplementedError("The method update_contact() is not yet implemented.")

    async def delete_contact(self, user_id: str, contact_id: str) -> Dict[str, Any]:
        """Delete a specific contact for a user by contact ID. Placeholder until implemented."""
        raise NotImplementedError("The method delete_contact() is not yet implemented.")

    async def count_contacts_for_user(self, user_id: str) -> Dict[str, Any]:
        """Count the contacts for a specific user. Placeholder until implemented."""
        raise NotImplementedError(
            "The method count_contacts_for_user() is not yet implemented."
        )

    async def get_my_contacts(self) -> Dict[str, Any]:
        """Retrieve contacts for the authenticated user. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_my_contacts() is not yet implemented."
        )


class SharedContactManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the SharedContactManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def get_domain_contacts(self, domain: str) -> Dict[str, Any]:
        """Retrieve all shared contacts for a specific domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_domain_contacts() is not yet implemented."
        )

    async def create_shared_contact(
        self, domain: str, contact_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new shared contact within a domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method create_shared_contact() is not yet implemented."
        )

    async def get_specific_domain_contact(
        self, domain: str, contact_id: str
    ) -> Dict[str, Any]:
        """Retrieve a specific shared contact in a domain by contact ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_specific_domain_contact() is not yet implemented."
        )

    async def update_shared_contact(
        self, domain: str, contact_id: str, contact_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a shared contact in a domain by contact ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_shared_contact() is not yet implemented."
        )

    async def delete_shared_contact(
        self, domain: str, contact_id: str
    ) -> Dict[str, Any]:
        """Delete a specific shared contact in a domain by contact ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method delete_shared_contact() is not yet implemented."
        )
