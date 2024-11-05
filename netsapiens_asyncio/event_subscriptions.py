from typing import Dict, Any, Optional, List
from .auth import AuthBase


class EventSubscriptionManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the EventSubscriptionManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def create_subscription(
        self,
        domain: str,
        model: str,
        post_url: str,
        user: str = "*",
        subscription_geo_support: str = "yes",
        reseller: Optional[str] = None,
        preferred_server: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new event subscription."""
        url = f"{self.server_url}/ns-api/v2/subscriptions"
        headers = await self.auth.get_headers()

        data = {
            "subscription-geo-support": subscription_geo_support,
            "domain": domain,
            "user": user,
            "model": model,
            "post-url": post_url,
        }

        if reseller:
            data["reseller"] = reseller
        if preferred_server:
            data["preferred-server"] = preferred_server

        return await self.auth._request("POST", url, headers=headers, json=data)

    async def read_subscriptions(self) -> List[Dict[str, Any]]:
        """Read all event subscriptions. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_subscriptions() is not yet implemented."
        )

    async def read_subscription_by_id(self, subscription_id: str) -> Dict[str, Any]:
        """Read event subscription by ID. Placeholder until implemented."""
        raise NotImplementedError(
            f"The method read_subscription_by_id() is not yet implemented. {subscription_id}"
        )

    async def update_subscription(
        self, subscription_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an event subscription by ID. Placeholder until implemented."""
        raise NotImplementedError(
            f"The method update_subscription() is not yet implemented. {subscription_id} {data}"
        )

    async def delete_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Delete an event subscription by ID. Placeholder until implemented."""
        raise NotImplementedError(
            f"The method delete_subscription() is not yet implemented. {subscription_id}"
        )
