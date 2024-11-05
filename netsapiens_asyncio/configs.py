from typing import Dict, Any
from .auth import AuthBase


class ConfigurationManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the ConfigurationManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def read_specific_configuration(self, config_id: str) -> Dict[str, Any]:
        """Retrieve details of a specific configuration by ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_specific_configuration() is not yet implemented."
        )

    async def delete_configuration(self, config_id: str) -> Dict[str, Any]:
        """Delete a specific configuration by ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method delete_configuration() is not yet implemented."
        )

    async def read_all_configurations(self) -> Dict[str, Any]:
        """Retrieve all configurations in the system. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_all_configurations() is not yet implemented."
        )

    async def create_configuration(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new configuration. Placeholder until implemented."""
        raise NotImplementedError(
            "The method create_configuration() is not yet implemented."
        )

    async def update_configuration(
        self, config_id: str, config_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific configuration by ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_configuration() is not yet implemented."
        )

    async def update_ns_api_configuration(
        self, ns_config_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update the Netsapiens API configuration. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_ns_api_configuration() is not yet implemented."
        )

    async def read_all_ns_api_configurations(self) -> Dict[str, Any]:
        """Retrieve all Netsapiens API configurations. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_all_ns_api_configurations() is not yet implemented."
        )


class DefinitionManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the DefinitionManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def read_all_definitions(self) -> Dict[str, Any]:
        """Retrieve all configuration definitions in the system. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_all_definitions() is not yet implemented."
        )

    async def create_definition(
        self, definition_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new configuration definition. Placeholder until implemented."""
        raise NotImplementedError(
            "The method create_definition() is not yet implemented."
        )

    async def read_specific_definition(self, definition_id: str) -> Dict[str, Any]:
        """Retrieve a specific configuration definition by ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_specific_definition() is not yet implemented."
        )

    async def update_definition(
        self, definition_id: str, definition_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific configuration definition by ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_definition() is not yet implemented."
        )

    async def delete_definition(self, definition_id: str) -> Dict[str, Any]:
        """Delete a specific configuration definition by ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method delete_definition() is not yet implemented."
        )
