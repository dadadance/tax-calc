"""RS.ge API integration module."""
from tax_core.rs_ge.api_client import RSGeAPIClient
from tax_core.rs_ge.auth import RSGeAuth
from tax_core.rs_ge.data_mapper import map_to_user_profile
from tax_core.rs_ge.exceptions import (
    RSGeAPIError,
    RSGeAuthError,
    RSGeDataError,
)

__all__ = [
    "RSGeAPIClient",
    "RSGeAuth",
    "map_to_user_profile",
    "RSGeAPIError",
    "RSGeAuthError",
    "RSGeDataError",
]

