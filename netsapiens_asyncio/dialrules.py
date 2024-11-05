from typing import Dict, Any
from .auth import AuthBase


class DialRuleManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the DialRuleManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def read_dialrules_in_dialplan(self, dialplan_id: str) -> Dict[str, Any]:
        """Retrieve all dial rules in a specific dial plan. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_dialrules_in_dialplan() is not yet implemented."
        )

    async def add_dialrule_to_dialplan(
        self, dialplan_id: str, rule_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a new dial rule to a specific dial plan. Placeholder until implemented."""
        raise NotImplementedError(
            "The method add_dialrule_to_dialplan() is not yet implemented."
        )

    async def read_specific_dialrule_in_dialplan(
        self, dialplan_id: str, rule_id: str
    ) -> Dict[str, Any]:
        """Retrieve a specific dial rule in a dial plan by rule ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_specific_dialrule_in_dialplan() is not yet implemented."
        )

    async def update_dialrule_in_dialplan(
        self, dialplan_id: str, rule_id: str, rule_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a specific dial rule in a dial plan by rule ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method update_dialrule_in_dialplan() is not yet implemented."
        )

    async def delete_dialrule_in_dialplan(
        self, dialplan_id: str, rule_id: str
    ) -> Dict[str, Any]:
        """Delete a specific dial rule in a dial plan by rule ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method delete_dialrule_in_dialplan() is not yet implemented."
        )
