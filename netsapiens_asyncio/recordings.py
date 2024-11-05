from typing import Dict, Any
from .auth import AuthBase


class RecordingManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the RecordingManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def get_recording_by_callid_for_user(
        self, call_id: str, user_id: str
    ) -> Dict[str, Any]:
        """Retrieve a specific recording by call ID for a specific user. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_recording_by_callid_for_user() is not yet implemented."
        )

    async def get_recording_by_callid_for_domain(
        self, call_id: str, domain: str
    ) -> Dict[str, Any]:
        """Retrieve a specific recording by call ID for a specific domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_recording_by_callid_for_domain() is not yet implemented."
        )
