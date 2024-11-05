from typing import Dict, Any
from .auth import AuthBase


class DomainManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the DomainManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def get_domains(self) -> Dict[str, Any]:
        """Retrieve all domains. Placeholder until implemented."""
        raise NotImplementedError("The method get_domains() is not yet implemented.")

    async def create_domain(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new domain. Placeholder until implemented."""
        raise NotImplementedError("The method create_domain() is not yet implemented.")

    async def count_domains(self) -> Dict[str, Any]:
        """Count all domains. Placeholder until implemented."""
        raise NotImplementedError("The method count_domains() is not yet implemented.")

    async def get_specific_domain(self, domain_id: str) -> Dict[str, Any]:
        """Retrieve a specific domain by ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_specific_domain() is not yet implemented."
        )

    async def update_domain(
        self, domain_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing domain. Placeholder until implemented."""
        raise NotImplementedError("The method update_domain() is not yet implemented.")

    async def delete_domain(self, domain_id: str) -> Dict[str, Any]:
        """Delete a domain by ID. Placeholder until implemented."""
        raise NotImplementedError("The method delete_domain() is not yet implemented.")

    async def get_specific_domain_with_billing_summary(
        self, domain_id: str
    ) -> Dict[str, Any]:
        """Retrieve a specific domain with billing summary by ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_specific_domain_with_billing_summary() is not yet implemented."
        )

    async def get_my_domain_info(self) -> Dict[str, Any]:
        """Retrieve information about the current domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_my_domain_info() is not yet implemented."
        )

    async def check_if_domain_exists(self, domain_name: str) -> Dict[str, Any]:
        """Check if a domain exists. Placeholder until implemented."""
        raise NotImplementedError(
            "The method check_if_domain_exists() is not yet implemented."
        )
