import aiohttp
import logging
from typing import Optional, Union
from .auth import NetsapiensAPI


class MessageAPI:
    def __init__(self, auth_client: NetsapiensAPI, log_level=logging.INFO):
        """
        Initialize the MessageAPI class with authentication details and logging setup.

        :param auth_client: Instance of NetsapiensAPI for managing authentication.
        :param log_level: Logging level (default is INFO).
        """
        self.auth_client = auth_client
        self.auth_data = self.auth_client.token_data
        self.base_url = self.auth_data.get("api_url") if self.auth_data else None
        self.domain = "~"
        self.user = "~"

        # Create a dedicated logger for this class
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        # Add a handler if the logger has no handlers (to avoid duplicate logs)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.debug("MessageAPI initialized with auth client")

    async def send_message(
        self,
        message_type: str,
        message: str,
        destination: Union[str, list],
        from_number: str,
        data: Optional[str] = None,
        mime_type: Optional[str] = None,
        size: Optional[int] = None,
    ):
        """
        Send a new message session via the API.

        :param message_type: Type of message to send (e.g., sms, mms).
        :param message: The text of the message to be sent.
        :param destination: A single recipient (str) or a list of recipients (List[str]).
        :param from_number: Sender's phone number (required for SMS).
        :param data: Base64-encoded data for MMS or media chat.
        :param mime_type: Mime type of the media file for MMS or media chat.
        :param size: Size of the media file in bytes for MMS or media chat.
        :return: API response as a dictionary.
        """
        # Check and refresh token if necessary
        self.auth_data = await self.auth_client.check_token_expiry()
        if not self.auth_data:
            self.logger.error(
                "Authentication data is not available. Cannot send message."
            )
            raise Exception("Authentication data is not available.")

        self.base_url = self.auth_data.get("api_url")

        url = f"{self.base_url}/ns-api/v2/domains/{self.domain}/users/{self.user}/messages"
        payload = {
            "type": message_type,
            "message": message,
            "destination": (
                destination if isinstance(destination, list) else [destination]
            ),
            "from-number": from_number,
        }

        # Add optional parameters if applicable
        if data:
            payload["data"] = data
        if mime_type:
            payload["mime-type"] = mime_type
        if size:
            payload["size"] = str(size)

        self.logger.debug(f"Sending message with payload: {payload}")

        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.auth_data['access_token']}"}
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    self.logger.info(f"Message sent successfully: {result}")
                    return result
                else:
                    error_message = await response.text()
                    self.logger.error(f"Failed to send message: {error_message}")
                    raise Exception(f"Failed to send message: {error_message}")
