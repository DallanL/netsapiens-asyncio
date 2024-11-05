from typing import Dict, Any
from .auth import AuthBase


class PhoneNumberUseCaseManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the PhoneNumberUseCaseManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def send_to_call_queue(
        self, phone_number_id: str, queue_id: str
    ) -> Dict[str, Any]:
        """Send a phone number to a call queue. Placeholder until implemented."""
        raise NotImplementedError(
            "The method send_to_call_queue() is not yet implemented."
        )

    async def send_to_user(self, phone_number_id: str, user_id: str) -> Dict[str, Any]:
        """Send a phone number to a specific user. Placeholder until implemented."""
        raise NotImplementedError("The method send_to_user() is not yet implemented.")

    async def send_to_offnet_number(
        self, phone_number_id: str, offnet_number: str
    ) -> Dict[str, Any]:
        """Send a phone number to an offnet (external) number. Placeholder until implemented."""
        raise NotImplementedError(
            "The method send_to_offnet_number() is not yet implemented."
        )

    async def set_to_available(self, phone_number_id: str) -> Dict[str, Any]:
        """Set a phone number to available. Placeholder until implemented."""
        raise NotImplementedError(
            "The method set_to_available() is not yet implemented."
        )
