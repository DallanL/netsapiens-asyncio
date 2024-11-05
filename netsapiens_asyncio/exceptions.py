class NetsapiensAPIError(Exception):
    """Base exception for Netsapiens API errors."""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Error {code}: {message}")


class BadRequestError(NetsapiensAPIError):
    """Exception for 400 Bad Request errors."""

    pass


class AuthenticationError(NetsapiensAPIError):
    """Exception for 401 Authentication Required errors."""

    pass


class ForbiddenError(NetsapiensAPIError):
    """Exception for 403 Forbidden errors."""

    pass


class NotFoundError(NetsapiensAPIError):
    """Exception for 404 Record Not Found errors."""

    pass
