from typing import Dict, Any
from .auth import AuthBase


class PhoneManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the PhoneManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def read_mac_addresses(self) -> Dict[str, Any]:
        """Retrieve all MAC addresses. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_mac_addresses() is not yet implemented."
        )

    async def add_mac_address(self, mac_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new MAC address. Placeholder until implemented."""
        raise NotImplementedError(
            "The method add_mac_address() is not yet implemented."
        )

    async def update_mac_address(
        self, mac_id: str, mac_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific MAC address. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_mac_address() is not yet implemented."
        )

    async def remove_mac_address(self, mac_id: str) -> Dict[str, Any]:
        """Remove a specific MAC address. Placeholder until implemented."""
        raise NotImplementedError(
            "The method remove_mac_address() is not yet implemented."
        )

    async def read_mac_addresses_in_domain(self, domain: str) -> Dict[str, Any]:
        """Retrieve MAC addresses within a specific domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_mac_addresses_in_domain() is not yet implemented."
        )

    async def add_mac_address_for_domain(
        self, domain: str, mac_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a new MAC address within a specific domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method add_mac_address_for_domain() is not yet implemented."
        )

    async def update_mac_address_in_domain(
        self, domain: str, mac_id: str, mac_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a MAC address within a specific domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_mac_address_in_domain() is not yet implemented."
        )

    async def remove_mac_address_in_domain(
        self, domain: str, mac_id: str
    ) -> Dict[str, Any]:
        """Remove a MAC address within a specific domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method remove_mac_address_in_domain() is not yet implemented."
        )

    async def read_specific_mac_address(self, mac_id: str) -> Dict[str, Any]:
        """Retrieve details for a specific MAC address. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_specific_mac_address() is not yet implemented."
        )

    async def get_supported_models(self) -> Dict[str, Any]:
        """Retrieve a list of supported phone models. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_supported_models() is not yet implemented."
        )

    async def get_supported_vendors(self) -> Dict[str, Any]:
        """Retrieve a list of supported phone vendors. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_supported_vendors() is not yet implemented."
        )

    async def get_model_details(self, model_id: str) -> Dict[str, Any]:
        """Retrieve details of a specific phone model. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_model_details() is not yet implemented."
        )

    async def get_server_profiles(self) -> Dict[str, Any]:
        """Retrieve a list of server profiles. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_server_profiles() is not yet implemented."
        )

    async def read_provisionable_server_details(self, server_id: str) -> Dict[str, Any]:
        """Retrieve details for a provisionable server. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_provisionable_server_details() is not yet implemented."
        )
