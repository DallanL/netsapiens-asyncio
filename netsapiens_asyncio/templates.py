from typing import Dict, Any
from .auth import AuthBase


class TemplateManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the TemplateManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def read_template(self, template_id: str) -> Dict[str, Any]:
        """Retrieve details of a specific template by ID. Placeholder until implemented."""
        raise NotImplementedError("The method read_template() is not yet implemented.")

    async def create_template_from_upload_base64(
        self, template_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new template from a JSON + Base64 upload. Placeholder until implemented."""
        raise NotImplementedError(
            "The method create_template_from_upload_base64() is not yet implemented."
        )

    async def delete_template(self, template_id: str) -> Dict[str, Any]:
        """Delete a specific template by ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method delete_template() is not yet implemented."
        )

    async def update_template_from_upload_base64(
        self, template_id: str, template_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing template from a JSON + Base64 upload. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_template_from_upload_base64() is not yet implemented."
        )
