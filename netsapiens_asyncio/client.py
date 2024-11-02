import httpx
from .exceptions import NetsapiensAPIError


class NetsapiensAsyncClient:
    def __init__(self, server_url: str, api_key: str):
        """
        Initialize the client with the server URL and API key.

        Args:
            server_url (str): The base URL of the Netsapiens API server.
            api_key (str): The API key for authorization.
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.api_key = api_key
        self._session = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "accept": "application/json",
            }
        )
        self.api_info = None  # Will hold API key info metadata after initialization

    async def initialize(self):
        """Verify the API key by calling `apikeys#1` and store the info."""
        url = f"https://{self.server_url}/ns-api/v2/apikeys#1"
        try:
            self.api_info = await self._request("GET", url)
            return {"api_key": self.api_key, "info": self.api_info}
        except NetsapiensAPIError as e:
            print(f"Failed to initialize client: {e}")
            raise

    async def _request(self, method: str, url: str, **kwargs):
        """Helper method to manage HTTP requests."""
        try:
            response = await self._session.request(method, url, **kwargs)
            response.raise_for_status()  # Raise error for HTTP error statuses (4xx, 5xx)
            return response.json()  # Return JSON response data
        except httpx.HTTPStatusError as exc:
            # Handle HTTP errors
            raise NetsapiensAPIError(
                f"HTTP error {exc.response.status_code} for {exc.request.url}: {exc.response.text}"
            ) from exc
        except Exception as exc:
            # Catch other unexpected errors
            raise NetsapiensAPIError(
                "An error occurred while processing the request"
            ) from exc

    async def get_user_info(self, user_id: str):
        """Fetch information for a specific user by ID.

        Args:
            user_id (str): The ID of the user to retrieve information for.

        Returns:
            dict: JSON response with user information.
        """
        url = f"https://{self.server_url}/ns-api/v2/users/{user_id}"
        return await self._request("GET", url)

    async def close(self):
        """Close the session gracefully."""
        await self._session.aclose()
