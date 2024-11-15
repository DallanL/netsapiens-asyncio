from typing import Optional, Dict, Any, List
from .auth import AuthBase
import logging

logger = logging.getLogger(__name__)


class MessageManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the MessageManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        logger.debug("Initializing MessageManager")
        logger.debug(f"Server URL: {server_url}")

        self.server_url = server_url.rstrip("/")
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
        logging.debug(f"{user_id} {message_data}")
        raise NotImplementedError(
            "The method send_message_chat() is not yet implemented."
        )

    async def send_message_group_chat(
        self, group_id: str, message_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send a message in a group chat. Placeholder until implemented."""
        logging.debug(f"{group_id} {message_data}")
        raise NotImplementedError(
            "The method send_message_group_chat() is not yet implemented."
        )

    async def send_message_media_chat(
        self, user_id: str, media_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send a media message in a chat session. Placeholder until implemented."""
        logging.debug(f"{user_id} {media_data}")
        raise NotImplementedError(
            "The method send_message_media_chat() is not yet implemented."
        )

    async def send_message_sms(
        self,
        domain: str,
        user: str,
        messagesession: str,
        message: str,
        destination: List[str],
        from_number: str,
    ) -> Dict[str, Any]:
        """
        Send an SMS message within a specified message session, supporting both v1 and v2 APIs.

        Args:
            domain (str): Domain name for the organization.
            user (str): User extension for the account.
            messagesession (str): Unique identifier of the message session (at least 32 alphanumeric characters).
            message (str): The message text to be sent.
            destination (List[str]): List of phone numbers or users to receive the message.
            from_number (str): The sender's number for outbound SMS.

        Returns:
            Dict[str, Any]: JSON response indicating the result of the message send operation.

        Raises:
            Exception: If an error occurs during the request.
        """
        # Log method entry and input arguments
        logging.debug("Entering send_message_sms")
        logging.debug(f"Domain: {domain}")
        logging.debug(f"User: {user}")
        logging.debug(f"Message Session: {messagesession}")
        logging.debug(f"Message: {message}")
        logging.debug(f"Destination: {destination}")
        logging.debug(f"From Number: {from_number}")

        # Determine if we're using v1 or v2 API based on the `apiv1` flag
        token_info = await self.auth.get_token_info()
        logging.debug(f"Token Info: {token_info}")

        if token_info.get("apiv1", False):
            # v1 API format
            url = f"{self.server_url}/ns-api/"
            payload = {
                "object": "message",
                "action": "create",
                "domain": domain,
                "user": user,
                "type": "sms",
                "session_id": messagesession,
                "from_num": from_number,
                "destination": ",".join(destination),
                "message": message,
            }
            logging.debug("Using v1 API format")
            logging.debug(f"URL: {url}")
            logging.debug(f"Payload (form data): {payload}")

            # Send request with multipart form data
            response = await self.auth._request("POST", url, data=payload)
        else:
            # v2 API format
            url = f"{self.server_url}/ns-api/v2/domains/{domain}/users/{user}/messagesessions/{messagesession}/messages"
            payload = {
                "type": "sms",
                "message": message,
                "destination": destination,
                "from-number": from_number,
            }
            logging.debug("Using v2 API format")
            logging.debug(f"URL: {url}")
            logging.debug(f"Payload (JSON): {payload}")

            # Send request with JSON payload
            response = await self.auth._request("POST", url, json=payload)

        # Log response details
        logging.debug("Response received")
        logging.debug(f"Response Status Code: {response.get('status_code')}")
        logging.debug(f"Response Headers: {response.get('headers')}")
        logging.debug(
            f"Response Content: {response.get('text') or response.get('json')}"
        )

        return response

    async def send_message_mms(
        self, phone_number: str, mms_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send an MMS message. Placeholder until implemented."""
        logging.debug(f"{phone_number} {mms_data}")
        raise NotImplementedError(
            "The method send_message_mms() is not yet implemented."
        )

    async def update_messagesession_participants(
        self, session_id: str, participants_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update participants in a message session. Placeholder until implemented."""
        logging.debug(f"{session_id} {participants_data}")
        raise NotImplementedError(
            "The method update_messagesession_participants() is not yet implemented."
        )

    async def delete_messagesession(self, session_id: str) -> Dict[str, Any]:
        """Delete a specific message session. Placeholder until implemented."""
        logging.debug(f"{session_id}")
        raise NotImplementedError(
            "The method delete_messagesession() is not yet implemented."
        )

    async def update_messagesession_name(
        self, session_id: str, name_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update the name of a message session. Placeholder until implemented."""
        logging.debug(f"{session_id} {name_data}")
        raise NotImplementedError(
            "The method update_messagesession_name() is not yet implemented."
        )

    async def update_messagesession_leave(self, session_id: str) -> Dict[str, Any]:
        """Leave a message session. Placeholder until implemented."""
        logging.debug(f"{session_id}")
        raise NotImplementedError(
            "The method update_messagesession_leave() is not yet implemented."
        )

    async def get_messagesessions_for_domain(self, domain: str) -> Dict[str, Any]:
        """Retrieve all message sessions for a specific domain. Placeholder until implemented."""
        logging.debug(f"{domain}")
        raise NotImplementedError(
            "The method get_messagesessions_for_domain() is not yet implemented."
        )

    async def start_new_message_session(
        self,
        domain: str,
        user: str,
        type: str,
        message: str,
        destination: List[str],
        from_number: Optional[str] = None,
        data: Optional[str] = None,
        mime_type: Optional[str] = None,
        size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Start a new message session and send an initial message.

        Args:
            domain (str): Domain name for the organization.
            user (str): User extension for the account.
            type (str): Type of message to send (e.g., 'sms', 'mms', 'chat').
            message (str): The message text to be sent.
            destination (List[str]): List of phone numbers or users to receive the message.
            from_number (Optional[str]): The sender's number for SMS (optional).
            data (Optional[str]): Base64-encoded data for media (used only for MMS or media chat).
            mime_type (Optional[str]): MIME type of the media file (used only for MMS or media chat).
            size (Optional[int]): Size in bytes of the media file (used only for MMS or media chat).

        Returns:
            Dict[str, Any]: JSON response indicating the result of starting the session and sending the message.

        Raises:
            Exception: If an error occurs during the request.
        """
        # Construct URL for starting a new message session
        url = f"{self.server_url}/ns-api/v2/domains/{domain}/users/{user}/messages"
        logger.debug(f"Constructed URL: {url}")

        # Construct the request body
        payload = {"type": type, "message": message, "destination": destination}
        if from_number:
            payload["from-number"] = from_number
        if data:
            payload["data"] = data
        if mime_type:
            payload["mime-type"] = mime_type
        if size:
            payload["size"] = size

        # Log the payload details
        logger.debug("Starting a new message session with the following details:")
        logger.debug(f"Domain: {domain}, User: {user}")
        logger.debug(f"Message Type: {type}")
        logger.debug(f"Message: {message}")
        logger.debug(f"Destination: {destination}")
        if from_number:
            logger.debug(f"From Number: {from_number}")
        if data:
            logger.debug(
                f"Data (Base64): {data[:50]}..."
            )  # Log only the first 50 chars for brevity
        if mime_type:
            logger.debug(f"MIME Type: {mime_type}")
        if size:
            logger.debug(f"Size: {size}")

        try:
            # Send the request and log the response
            logger.debug("Sending request to start a new message session...")
            response = await self.auth._request("POST", url, json=payload)
            logger.debug(f"Response received: {response}")
            return response

        except Exception as e:
            # Log any errors encountered during the request
            logger.error("An error occurred while starting a new message session")
            logger.error(f"Error details: {str(e)}")
            raise e
