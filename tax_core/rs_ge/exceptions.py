"""Custom exceptions for RS.ge integration."""


class RSGeError(Exception):
    """Base exception for RS.ge integration errors."""
    pass


class RSGeAPIError(RSGeError):
    """Error when making API requests to RS.ge."""
    pass


class RSGeAuthError(RSGeError):
    """Error during authentication with RS.ge."""
    pass


class RSGeDataError(RSGeError):
    """Error when processing or mapping RS.ge data."""
    pass


class RSGeConnectionError(RSGeAPIError):
    """Error when connection to RS.ge fails."""
    pass


class RSGeRateLimitError(RSGeAPIError):
    """Error when RS.ge API rate limit is exceeded."""
    pass

