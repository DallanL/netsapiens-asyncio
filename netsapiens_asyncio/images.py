from typing import Dict, Any
from .auth import AuthBase


class ImageManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the ImageManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def read_image(self, image_id: str) -> Dict[str, Any]:
        """Retrieve details of a specific image by ID. Placeholder until implemented."""
        raise NotImplementedError("The method read_image() is not yet implemented.")

    async def create_image_from_upload_base64(
        self, image_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new image from a JSON + Base64 upload. Placeholder until implemented."""
        raise NotImplementedError(
            "The method create_image_from_upload_base64() is not yet implemented."
        )

    async def delete_image(self, image_id: str) -> Dict[str, Any]:
        """Delete a specific image by ID. Placeholder until implemented."""
        raise NotImplementedError("The method delete_image() is not yet implemented.")

    async def update_image_from_upload_multipart(
        self, image_id: str, image_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing image from a multipart/mixed upload. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_image_from_upload_multipart() is not yet implemented."
        )

    async def create_image_from_upload_multipart(
        self, image_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new image from a multipart/mixed upload. Placeholder until implemented."""
        raise NotImplementedError(
            "The method create_image_from_upload_multipart() is not yet implemented."
        )

    async def update_image_from_upload_base64(
        self, image_id: str, image_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing image from a JSON + Base64 upload. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_image_from_upload_base64() is not yet implemented."
        )
