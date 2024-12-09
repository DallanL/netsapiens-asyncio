import aiohttp
from datetime import datetime
import logging
from typing import Optional, Dict, Union
from .auth import NetsapiensAPI


class SubscriptionAPI:
    VALID_MODELS = [
        "agent",
        "auditlog",
        "auditlog_lite",
        "call",
        "call_origid",
        "cdr",
        "message",
        "messagesession",
        "subscriber",
        "presence",
        "voicemail",
    ]

    def __init__(self, auth_client: NetsapiensAPI, log_level=logging.INFO):
        """
        Initialize the SubscriptionAPI class with authentication details and logging setup.

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

        self.logger.debug("SubscriptionAPI initialized with auth client")

    async def create_subscription(
        self,
        model: str,
        post_url: str,
        subscription_geo_support: Optional[str] = "yes",
        reseller: Optional[str] = "*",
        domain: Optional[str] = "*",
        user: Optional[str] = "*",
        preferred_server: Optional[str] = None,
    ) -> Dict:
        """
        Create a new event subscription.

        :param model: The type of data the subscription will send (e.g., call, cdr, message).
        :param post_url: The URL where the API will post data. Must include a valid protocol (https:// or http://).
        :param subscription_geo_support: Optional. Defaults to "yes".
        :param reseller: Optional. Defaults to "*", indicating all resellers (requires Super User scope).
        :param domain: Optional. Defaults to "*", indicating all domains (requires Super User scope).
        :param user: Optional. Defaults to "*", indicating all users.
        :param preferred_server: Optional. A specific server hostname to use as the preferred server.
        :return: A dictionary containing the subscription details.
        """

        # Validate model
        if model not in self.VALID_MODELS:
            self.logger.error(
                f"Invalid model '{model}'. Must be one of: {', '.join(self.VALID_MODELS)}"
            )
            raise ValueError(
                f"Invalid model '{model}'. Must be one of: {', '.join(self.VALID_MODELS)}"
            )

        # Refresh token if necessary
        self.auth_data = await self.auth_client.check_token_expiry()
        if not self.auth_data:
            self.logger.error(
                "Authentication data is not available. Cannot create subscription."
            )
            raise Exception("Authentication data is not available.")

        self.base_url = self.auth_data.get("api_url")
        url = f"{self.base_url}/ns-api/v2/subscriptions"

        # Construct payload
        payload = {
            "model": model,
            "post-url": post_url,
            "subscription-geo-support": subscription_geo_support,
            "reseller": reseller,
            "domain": domain,
            "user": user,
        }
        if preferred_server:
            payload["preferred-server"] = preferred_server

        self.logger.debug(f"Creating subscription with payload: {payload}")

        # Make POST request
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.auth_data['access_token']}"}
            try:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.logger.info(f"Subscription created successfully: {result}")
                        return result
                    else:
                        error_message = await response.text()
                        self.logger.error(
                            f"Failed to create subscription. "
                            f"Status: {response.status}, Error: {error_message}"
                        )
                        raise Exception(
                            f"Failed to create subscription: {error_message}"
                        )
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error while creating subscription: {e}")
                raise Exception(
                    "Network error occurred while creating subscription."
                ) from e
            except Exception as e:
                self.logger.error(f"Unexpected error while creating subscription: {e}")
                raise Exception(
                    "An unexpected error occurred while creating subscription."
                ) from e

    async def read_subscription(
        self, subscription_id: Optional[str] = None
    ) -> Union[dict, list[dict]]:
        """
        Retrieve event subscriptions. If subscription_id is provided, fetches the details for that specific subscription.
        If no subscription_id is provided, retrieves all subscriptions.

        :param subscription_id: Optional. The ID of the subscription to retrieve.
        :return: A dictionary for a specific subscription or a list of dictionaries for all subscriptions.
        """
        # Refresh token if necessary
        self.auth_data = await self.auth_client.check_token_expiry()
        if not self.auth_data:
            self.logger.error(
                "Authentication data is not available. Cannot retrieve subscription(s)."
            )
            raise Exception("Authentication data is not available.")

        self.base_url = self.auth_data.get("api_url")

        # Construct URL based on whether subscription_id is provided
        if subscription_id:
            url = f"{self.base_url}/ns-api/v2/subscriptions/{subscription_id}"
        else:
            url = f"{self.base_url}/ns-api/v2/subscriptions"

        self.logger.debug(f"Retrieving subscription(s) from {url}")

        # Make GET request
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.auth_data['access_token']}"}
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        if subscription_id:
                            self.logger.info(
                                f"Subscription {subscription_id} retrieved successfully."
                            )
                        else:
                            self.logger.info(
                                f"Subscriptions retrieved successfully: {len(result)} items found."
                            )
                        return result
                    else:
                        error_message = await response.text()
                        self.logger.error(
                            f"Failed to retrieve subscription(s). "
                            f"Status: {response.status}, Error: {error_message}"
                        )
                        raise Exception(
                            f"Failed to retrieve subscription(s): {error_message}"
                        )
            except aiohttp.ClientError as e:
                self.logger.error(
                    f"Network error while retrieving subscription(s): {e}"
                )
                raise Exception(
                    "Network error occurred while retrieving subscription(s)."
                ) from e
            except Exception as e:
                self.logger.error(
                    f"Unexpected error while retrieving subscription(s): {e}"
                )
                raise Exception(
                    "An unexpected error occurred while retrieving subscription(s)."
                ) from e

    async def update_subscription(
        self,
        subscription_id: str,
        model: Optional[str] = None,
        post_url: Optional[str] = None,
        subscription_geo_support: Optional[str] = None,
        subscription_expires_datetime: Optional[str] = None,
        preferred_server: Optional[str] = None,
        error_count: Optional[int] = None,
        posts_count: Optional[int] = None,
    ) -> dict:
        """
        Update an existing event subscription.

        :param subscription_id: The ID of the subscription to update.
        :param model: Optional. The type of data the subscription will send (e.g., call, cdr, message).
        :param post_url: Optional. The URL where the API will post data.
        :param subscription_geo_support: Optional. Whether geo support is enabled ("yes" or "no").
        :param subscription_expires_datetime: Optional. Expiration date-time in "YYYY-MM-DD HH:MM:SS" format.
        :param preferred_server: Optional. Preferred server hostname.
        :param error_count: Optional. Resets the error count if set to 0.
        :param posts_count: Optional. Resets the posts count if set to 0.
        :return: A dictionary containing the updated subscription details.
        """
        # Validate model
        if model not in self.VALID_MODELS:
            self.logger.error(
                f"Invalid model '{model}'. Must be one of: {', '.join(self.VALID_MODELS)}"
            )
            raise ValueError(
                f"Invalid model '{model}'. Must be one of: {', '.join(self.VALID_MODELS)}"
            )

        # Validate subscription ID
        if not subscription_id:
            self.logger.error("Subscription ID is required.")
            raise ValueError("Subscription ID is required.")

        # Validate datetime format
        if subscription_expires_datetime:
            try:
                datetime.strptime(subscription_expires_datetime, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                self.logger.error(
                    f"Invalid datetime format for subscription_expires_datetime: {subscription_expires_datetime}. "
                    f"Expected format is 'YYYY-MM-DD HH:MM:SS'."
                )
                raise ValueError(
                    "Invalid datetime format for subscription_expires_datetime. Expected format is 'YYYY-MM-DD HH:MM:SS'."
                )

        # Refresh token if necessary
        self.auth_data = await self.auth_client.check_token_expiry()
        if not self.auth_data:
            self.logger.error(
                "Authentication data is not available. Cannot update subscription."
            )
            raise Exception("Authentication data is not available.")

        self.base_url = self.auth_data.get("api_url")
        url = f"{self.base_url}/ns-api/v2/subscriptions/{subscription_id}"

        # Build the payload
        payload = {}
        if model:
            payload["model"] = model
        if post_url:
            payload["post-url"] = post_url
        if subscription_geo_support:
            payload["subscription-geo-support"] = subscription_geo_support
        if subscription_expires_datetime:
            payload["subscription-expires-datetime"] = subscription_expires_datetime
        if preferred_server:
            payload["preferred-server"] = preferred_server
        if error_count:
            payload["error-count"] = "0"
        if posts_count:
            payload["posts-count"] = "0"

        # Ensure there's data to update
        if not payload:
            self.logger.error("No data provided to update the subscription.")
            raise ValueError(
                "At least one field must be provided to update the subscription."
            )

        self.logger.debug(
            f"Updating subscription {subscription_id} with payload: {payload}"
        )

        # Make PUT request
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.auth_data['access_token']}"}
            try:
                async with session.put(url, json=payload, headers=headers) as response:
                    if response.status == 202:
                        result = await response.json()
                        self.logger.info(
                            f"Subscription {subscription_id} updated successfully: {result}"
                        )
                        return result
                    else:
                        error_message = await response.text()
                        self.logger.error(
                            f"Failed to update subscription {subscription_id}. "
                            f"Status: {response.status}, Error: {error_message}"
                        )
                        raise Exception(
                            f"Failed to update subscription: {error_message}"
                        )
            except aiohttp.ClientError as e:
                self.logger.error(
                    f"Network error while updating subscription {subscription_id}: {e}"
                )
                raise Exception(
                    "Network error occurred while updating subscription."
                ) from e
            except Exception as e:
                self.logger.error(
                    f"Unexpected error while updating subscription {subscription_id}: {e}"
                )
                raise Exception(
                    "An unexpected error occurred while updating subscription."
                ) from e

    async def delete_subscription(self, subscription_id: str) -> dict:
        """
        Delete an event subscription by its ID.

        :param subscription_id: The ID of the subscription to delete.
        :return: A dictionary containing the API response or confirmation message.
        """
        # Validate subscription ID
        if not subscription_id:
            self.logger.error("Subscription ID is required.")
            raise ValueError("Subscription ID is required.")

        # Refresh token if necessary
        self.auth_data = await self.auth_client.check_token_expiry()
        if not self.auth_data:
            self.logger.error(
                "Authentication data is not available. Cannot delete subscription."
            )
            raise Exception("Authentication data is not available.")

        self.base_url = self.auth_data.get("api_url")

        # Construct the URL
        url = f"{self.base_url}/ns-api/v2/subscriptions/{subscription_id}"
        self.logger.debug(f"Deleting subscription {subscription_id} at {url}")

        # Make DELETE request
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.auth_data['access_token']}"}
            try:
                async with session.delete(url, headers=headers) as response:
                    if response.status == 202:
                        result = await response.json()
                        self.logger.info(
                            f"Subscription {subscription_id} deleted successfully: {result}"
                        )
                        return result
                    else:
                        error_message = await response.text()
                        self.logger.error(
                            f"Failed to delete subscription {subscription_id}. "
                            f"Status: {response.status}, Error: {error_message}"
                        )
                        raise Exception(
                            f"Failed to delete subscription: {error_message}"
                        )
            except aiohttp.ClientError as e:
                self.logger.error(
                    f"Network error while deleting subscription {subscription_id}: {e}"
                )
                raise Exception(
                    "Network error occurred while deleting subscription."
                ) from e
            except Exception as e:
                self.logger.error(
                    f"Unexpected error while deleting subscription {subscription_id}: {e}"
                )
                raise Exception(
                    "An unexpected error occurred while deleting subscription."
                ) from e
