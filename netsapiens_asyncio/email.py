from typing import Dict, Any
from .auth import AuthBase


class EmailManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the EmailManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def send_email_using_template(
        self, template_id: str, email_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send an email using a specified template. Placeholder until implemented."""
        raise NotImplementedError(
            "The method send_email_using_template() is not yet implemented."
        )
