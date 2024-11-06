from typing import Optional, Dict, Any
from .auth import AuthBase


class MessageManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the MessageManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def get_messagesessions_for_user(
        self, domain: str = "~", user: str = "~", limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Retrieve message sessions for a specific user in a domain.

        Args:
            domain (str): Domain name for the organization. Use "~" for the domain linked to the token/key.
            user (str): User extension for the account. Use "~" for the user linked to the token/key.
            limit (Optional[int]): Optional limit for the number of message sessions to retrieve.

        Returns:
            Dict[str, Any]: JSON response containing message sessions.

        Raises:
            Exception: If an error occurs during the request.
        """
        url = (
            f"{self.server_url}/ns-api/v2/domains/{domain}/users/{user}/messagesessions"
        )
        params = {"limit": limit} if limit else {}

        response = await self.auth._request("GET", url, params=params)
        return response

    async def get_messages_for_session(
        self,
        domain: str = "~",
        user: str = "~",
        messagesession: str = "",
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve messages for a specific message session.

        Args:
            domain (str): Domain name for the organization. Use "~" for the domain linked to the token/key.
            user (str): User extension for the account. Use "~" for the user linked to the token/key.
            messagesession (str): Unique identifier of the message session.
            limit (Optional[int]): Optional limit for the number of messages to retrieve.

        Returns:
            Dict[str, Any]: JSON response containing messages in the session.

        Raises:
            Exception: If an error occurs during the request.
        """
        url = f"{self.server_url}/ns-api/v2/domains/{domain}/users/{user}/messagesessions/{messagesession}/messages"
        params = {"limit": limit} if limit else {}

        # Use auth to make the request
        response = await self.auth._request("GET", url, params=params)
        return response

    async def send_message_chat(
        self, user_id: str, message_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send a message in a chat session. Placeholder until implemented."""
        raise NotImplementedError(
            "The method send_message_chat() is not yet implemented."
        )

    async def send_message_group_chat(
        self, group_id: str, message_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send a message in a group chat. Placeholder until implemented."""
        raise NotImplementedError(
            "The method send_message_group_chat() is not yet implemented."
        )

    async def send_message_media_chat(
        self, user_id: str, media_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send a media message in a chat session. Placeholder until implemented."""
        raise NotImplementedError(
            "The method send_message_media_chat() is not yet implemented."
        )

    async def send_message_sms(
        self, phone_number: str, sms_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send an SMS message. Placeholder until implemented."""
        raise NotImplementedError(
            "The method send_message_sms() is not yet implemented."
        )

    async def send_message_group_sms(
        self, group_id: str, sms_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send a group SMS message. Placeholder until implemented."""
        raise NotImplementedError(
            "The method send_message_group_sms() is not yet implemented."
        )

    async def send_message_mms(
        self, phone_number: str, mms_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send an MMS message. Placeholder until implemented."""
        raise NotImplementedError(
            "The method send_message_mms() is not yet implemented."
        )

    async def update_messagesession_participants(
        self, session_id: str, participants_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update participants in a message session. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_messagesession_participants() is not yet implemented."
        )

    async def delete_messagesession(self, session_id: str) -> Dict[str, Any]:
        """Delete a specific message session. Placeholder until implemented."""
        raise NotImplementedError(
            "The method delete_messagesession() is not yet implemented."
        )

    async def update_messagesession_name(
        self, session_id: str, name_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update the name of a message session. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_messagesession_name() is not yet implemented."
        )

    async def update_messagesession_leave(self, session_id: str) -> Dict[str, Any]:
        """Leave a message session. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_messagesession_leave() is not yet implemented."
        )

    async def get_messagesessions_for_domain(self, domain: str) -> Dict[str, Any]:
        """Retrieve all message sessions for a specific domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method get_messagesessions_for_domain() is not yet implemented."
        )

    async def start_new_message_session(
        self, session_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Start a new message session. Placeholder until implemented."""
        raise NotImplementedError(
            "The method start_new_message_session() is not yet implemented."
        )
