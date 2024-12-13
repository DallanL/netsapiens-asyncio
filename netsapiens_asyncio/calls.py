import random
import string
from datetime import datetime, timezone
import aiohttp
import logging
from typing import Optional, Union
from .auth import NetsapiensAPI


class CallsAPI:
    def __init__(self, auth_client: NetsapiensAPI, log_level=logging.INFO):
        """
        Initialize the CallsAPI class with authentication details and logging setup.

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

        self.logger.debug("CallsAPI initialized with auth client")

    async def read_calls(
        self,
        domain: str,
        count: bool = False,
        user: Optional[str] = None,
        callid: Optional[str] = None,
    ) -> Union[dict, list]:
        """
        Retrieve active calls in the domain, for a specific user, or for a specific call ID.
        Optionally, retrieve the count of active calls.

        :param domain: The domain to query.
        :param count: If True, retrieve the count of active calls instead of detailed information.
        :param user: Optional. The user for whom to retrieve active calls. Defaults to None.
        :param callid: Optional. The specific call ID to retrieve. Defaults to None.
        :return: A dictionary or list of active calls based on the query.
        """
        # Validate parameter combinations
        if count and (user or callid):
            self.logger.error(
                "Invalid parameter combination: 'count' cannot be used with 'user' or 'callid'."
            )
            raise ValueError("'count' cannot be used with 'user' or 'callid'.")
        if callid and not user:
            self.logger.error(
                "Invalid parameter combination: 'callid' requires 'user' to be set."
            )
            raise ValueError("'callid' requires 'user' to be set.")

        # Check and refresh token if necessary
        self.auth_data = await self.auth_client.check_token_expiry()
        self.base_url = self.auth_data.get("api_url")

        # Build the base URL
        url = f"{self.base_url}/ns-api/v2/domains/{domain}"

        # Add optional path segments based on parameters
        if user:
            url += f"/users/{user}"
            if callid:
                url += f"/calls/{callid}"
        elif count:
            url += "/calls/count"
        else:
            url += "/calls"

        self.logger.debug(f"Retrieving calls from URL: {url}")

        # Make GET request
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.auth_data['access_token']}"}
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.logger.info(f"Calls retrieved successfully: {result}")
                        return result
                    else:
                        error_message = await response.text()
                        self.logger.error(
                            f"Failed to retrieve calls. Status: {response.status}, Error: {error_message}"
                        )
                        raise Exception(f"Failed to retrieve calls: {error_message}")
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error while retrieving calls: {e}")
                raise Exception("Network error occurred while retrieving calls.") from e
            except Exception as e:
                self.logger.error(f"Unexpected error while retrieving calls: {e}")
                raise Exception(
                    "An unexpected error occurred while retrieving calls."
                ) from e

    async def new_call(
        self,
        domain: str,
        user: str,
        synchronous: str,
        call_term_user: str,
        call_id: Optional[str] = None,
        dial_rule_application: Optional[str] = "call",
        call_orig_user: Optional[str] = None,
        auto_answer_enabled: Optional[str] = "no",
        caller_id_number: Optional[str] = None,
        callback_caller_id_number: Optional[str] = None,
    ) -> dict:
        """
        Make a new call via the API.

        :param domain: The domain in which the call is made.
        :param user: The user initiating the call.
        :param synchronous: Whether to wait for synchronous confirmation ("yes" or "no").
        :param call_id: A unique call ID for the new call. If not provided, it will be auto-generated.
        :param call_term_user: The destination/termination number for the call.
        :param dial_rule_application: Optional. Helps with next destination selection. Defaults to "call".
        :param call_orig_user: Optional. The origination user, device, or number. Defaults to user@domain.
        :param auto_answer_enabled: Optional. Whether auto-answer is enabled. Defaults to "no".
        :param caller_id_number: Optional. The caller ID for the termination leg.
        :param callback_caller_id_number: Optional. The caller ID for the origination leg callback.
        :return: A dictionary containing the response from the API.
        """
        # Validate synchronous parameter
        if synchronous not in {"yes", "no"}:
            self.logger.error("Invalid value for 'synchronous': must be 'yes' or 'no'.")
            raise ValueError("Invalid value for 'synchronous': must be 'yes' or 'no'.")

        # Generate call_id if not provided
        if not call_id:
            utc_timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
            random_suffix = "".join(
                random.choices(string.ascii_letters + string.digits, k=6)
            )
            call_id = f"nsaio{utc_timestamp}r{random_suffix}"
            self.logger.debug(f"Generated call_id: {call_id}")

        # Validate required parameters
        if not call_term_user:
            self.logger.error("The 'call_term_user' parameter is required.")
            raise ValueError("The 'call_term_user' parameter is required.")

        # Check and refresh token if necessary
        self.auth_data = await self.auth_client.check_token_expiry()
        self.base_url = self.auth_data.get("api_url")

        # Build the API URL
        url = f"{self.base_url}/ns-api/v2/domains/{domain}/users/{user}/calls"

        # Build the request payload
        payload = {
            "synchronous": synchronous,
            "call-id": call_id,
            "dial-rule-application": dial_rule_application,
            "call-term-user": call_term_user,
            "call-orig-user": call_orig_user or f"{user}@{domain}",
            "auto-answer-enabled": auto_answer_enabled,
        }
        if caller_id_number:
            payload["caller-id-number"] = caller_id_number
        if callback_caller_id_number:
            payload["callback-caller-id-number"] = callback_caller_id_number

        self.logger.debug(f"Making new call with payload: {payload}")

        # Make the POST request
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.auth_data['access_token']}"}
            try:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status in {200, 202}:
                        result = await response.json()
                        self.logger.info(f"Call created successfully: {result}")
                        return result
                    else:
                        error_message = await response.text()
                        self.logger.error(
                            f"Failed to create call. Status: {response.status}, Error: {error_message}"
                        )
                        raise Exception(f"Failed to create call: {error_message}")
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error while creating call: {e}")
                raise Exception("Network error occurred while creating call.") from e
            except Exception as e:
                self.logger.error(f"Unexpected error while creating call: {e}")
                raise Exception(
                    "An unexpected error occurred while creating call."
                ) from e
