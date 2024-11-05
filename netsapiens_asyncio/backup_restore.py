from typing import Dict, Any
from .auth import AuthBase


class BackupRestoreManager:
    def __init__(self, server_url: str, auth: AuthBase):
        """
        Initialize the BackupRestoreManager with server URL and auth.

        Args:
            server_url (str): Base URL of the Netsapiens API server.
            auth (AuthBase): An authentication instance (e.g., ApiKeyAuth or JWTAuth).
        """
        self.server_url = server_url.rstrip("/")  # Ensure no trailing slash
        self.auth = auth

    async def manually_backup_domain(self, domain: str) -> Dict[str, Any]:
        """Initiate a manual backup for a specific domain. Placeholder until implemented."""
        raise NotImplementedError(
            "The method manually_backup_domain() is not yet implemented."
        )

    async def request_full_system_backup(self) -> Dict[str, Any]:
        """Request a full system backup. Placeholder until implemented."""
        raise NotImplementedError(
            "The method request_full_system_backup() is not yet implemented."
        )

    async def read_available_restore_points(self) -> Dict[str, Any]:
        """Retrieve a list of available restore points. Placeholder until implemented."""
        raise NotImplementedError(
            "The method read_available_restore_points() is not yet implemented."
        )

    async def restore_specific_domain_backup(
        self, domain: str, restore_point_id: str
    ) -> Dict[str, Any]:
        """Restore a specific backup for a domain using a given restore point ID. Placeholder until implemented."""
        raise NotImplementedError(
            "The method restore_specific_domain_backup() is not yet implemented."
        )
