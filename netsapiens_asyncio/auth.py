import aiohttp
import logging
from datetime import datetime, timezone, timedelta


class NetsapiensAPI:
    def __init__(self, auth_config: dict, log_level=logging.INFO):
        """
        Initialize the NetsapiensAPI class with authentication details and logging setup.

        :param auth_config: Dictionary containing authentication information.
        :param log_level: Logging level (default is INFO).
        """
        self.base_url = auth_config.get("base_url")
        self.client_id = auth_config.get("client_id")
        self.client_secret = auth_config.get("client_secret")
        self.username = auth_config.get("username")
        self.password = auth_config.get("password")
        self.token_data = None

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

        self.logger.debug("NetsapiensAPI initialized")

    async def get_token(self):
        """
        Asynchronously request a new OAuth2 token using the password grant.

        :return: A dictionary containing the token data.
        """
        url = f"https://{self.base_url}/ns-api/v2/tokens"
        payload = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password,
        }
        self.logger.debug(f"Requesting token with payload: {payload}")

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    token_data = await response.json()
                    expires_in_seconds = token_data.get("expires_in", 0)
                    token_data["expires_at"] = (
                        datetime.now(timezone.utc)
                        + timedelta(seconds=expires_in_seconds)
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    token_data["api_url"] = f"https://{self.base_url}"
                    self.token_data = token_data
                    self.logger.info(
                        f"Received new auth token: {self.token_data['access_token']}"
                    )
                    return self.token_data
                else:
                    error_message = await response.text()
                    self.logger.error(f"Failed to get token: {error_message}")
                    raise Exception(f"Failed to get token: {error_message}")

    async def refresh_access_token(self):
        """
        Asynchronously refresh the OAuth2 token.

        :return: A dictionary containing the new token data.
        """
        if not self.token_data or "refresh_token" not in self.token_data:
            self.logger.error("No refresh token available. Please authenticate first.")
            raise Exception("No refresh token available. Please authenticate first.")

        url = f"https://{self.base_url}/ns-api/v2/tokens"
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.token_data["refresh_token"],
        }
        self.logger.debug(f"Refreshing token with payload: {payload}")

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    token_data = await response.json()
                    expires_in_seconds = token_data.get("expires_in", 0)
                    token_data["expires_at"] = (
                        datetime.now(timezone.utc)
                        + timedelta(seconds=expires_in_seconds)
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    token_data["api_url"] = f"https://{self.base_url}"
                    self.token_data = token_data
                    self.logger.info(
                        f"Token refreshed successfully: {self.token_data['access_token']}"
                    )
                    return self.token_data
                else:
                    error_message = await response.text()
                    self.logger.error(f"Failed to refresh token: {error_message}")
                    raise Exception(f"Failed to refresh token: {error_message}")

    async def check_token_expiry(self):
        """
        Check if the access token has expired. If expired, refresh it and update the token data.
        Raises an exception if token data or expires_at is not available.

        :return: Updated token data.
        """
        if not self.token_data:
            self.logger.error("Token data is not available. Please authenticate first.")
            raise Exception("Token data is missing. Authentication is required.")

        if "expires_at" not in self.token_data:
            self.logger.error(
                "'expires_at' is missing in token data. Authentication failed."
            )
            raise Exception(
                "'expires_at' is missing in token data. Cannot verify token validity."
            )

        # Parse the expiration time and make it timezone-aware
        try:
            expires_at = datetime.strptime(
                self.token_data["expires_at"], "%Y-%m-%d %H:%M:%S"
            ).replace(tzinfo=timezone.utc)
        except ValueError as e:
            self.logger.error(f"Invalid 'expires_at' format in token data: {e}")
            raise Exception("Invalid 'expires_at' format in token data.") from e

        now = datetime.now(timezone.utc)

        # Check if the token has expired
        if now >= expires_at:
            self.logger.info("Access token has expired. Refreshing token...")
            return await self.refresh_access_token()
        else:
            self.logger.info("Access token is still valid.")
            return self.token_data
