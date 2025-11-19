"""Authentication module for RS.ge API."""
import os
from typing import Optional, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
import requests
from tax_core.rs_ge.exceptions import RSGeAuthError, RSGeConnectionError


@dataclass
class AuthToken:
    """Authentication token for RS.ge API."""
    token: str
    expires_at: datetime
    token_type: str = "Bearer"
    
    def is_expired(self) -> bool:
        """Check if token is expired."""
        return datetime.now() >= self.expires_at
    
    def is_valid(self) -> bool:
        """Check if token is valid."""
        return not self.is_expired() and bool(self.token)


class RSGeAuth:
    """Handle authentication with RS.ge API."""
    
    # RS.ge API endpoints (to be updated with actual endpoints)
    AUTH_URL = "https://services.rs.ge/api/auth"  # Placeholder
    TOKEN_REFRESH_URL = "https://services.rs.ge/api/auth/refresh"  # Placeholder
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize RS.ge authentication.
        
        Args:
            username: RS.ge username (or from environment)
            password: RS.ge password (or from environment)
        """
        self.username = username or os.getenv("RS_GE_USERNAME")
        self.password = password or os.getenv("RS_GE_PASSWORD")
        self._token: Optional[AuthToken] = None
        
        if not self.username or not self.password:
            raise RSGeAuthError(
                "RS.ge credentials not provided. "
                "Set RS_GE_USERNAME and RS_GE_PASSWORD environment variables "
                "or provide username and password directly."
            )
    
    def authenticate(self) -> AuthToken:
        """
        Authenticate with RS.ge and obtain access token.
        
        Returns:
            AuthToken: Authentication token
            
        Raises:
            RSGeAuthError: If authentication fails
            RSGeConnectionError: If connection to RS.ge fails
        """
        try:
            # TODO: Implement actual RS.ge authentication
            # This is a placeholder implementation
            # RS.ge may use SOAP, OAuth, or custom authentication
            
            response = requests.post(
                self.AUTH_URL,
                json={
                    "username": self.username,
                    "password": self.password,
                },
                timeout=10,
            )
            
            if response.status_code == 200:
                data = response.json()
                token = AuthToken(
                    token=data.get("access_token", ""),
                    expires_at=datetime.now() + timedelta(seconds=data.get("expires_in", 3600)),
                    token_type=data.get("token_type", "Bearer"),
                )
                self._token = token
                return token
            elif response.status_code == 401:
                raise RSGeAuthError("Invalid RS.ge credentials")
            else:
                raise RSGeAuthError(f"Authentication failed: {response.status_code}")
                
        except requests.exceptions.ConnectionError as e:
            raise RSGeConnectionError(f"Failed to connect to RS.ge: {str(e)}")
        except requests.exceptions.Timeout as e:
            raise RSGeConnectionError(f"Connection to RS.ge timed out: {str(e)}")
        except Exception as e:
            raise RSGeAuthError(f"Authentication error: {str(e)}")
    
    def get_token(self) -> AuthToken:
        """
        Get valid authentication token, refreshing if necessary.
        
        Returns:
            AuthToken: Valid authentication token
        """
        if self._token is None or self._token.is_expired():
            return self.authenticate()
        return self._token
    
    def refresh_token(self) -> AuthToken:
        """
        Refresh the authentication token.
        
        Returns:
            AuthToken: New authentication token
            
        Raises:
            RSGeAuthError: If token refresh fails
        """
        if self._token is None:
            return self.authenticate()
        
        try:
            # TODO: Implement actual token refresh logic
            response = requests.post(
                self.TOKEN_REFRESH_URL,
                json={"refresh_token": self._token.token},
                timeout=10,
            )
            
            if response.status_code == 200:
                data = response.json()
                token = AuthToken(
                    token=data.get("access_token", ""),
                    expires_at=datetime.now() + timedelta(seconds=data.get("expires_in", 3600)),
                    token_type=data.get("token_type", "Bearer"),
                )
                self._token = token
                return token
            else:
                # If refresh fails, try full authentication
                return self.authenticate()
                
        except Exception as e:
            # If refresh fails, try full authentication
            return self.authenticate()
    
    def validate_credentials(self) -> bool:
        """
        Validate RS.ge credentials without storing token.
        
        Returns:
            bool: True if credentials are valid
        """
        try:
            token = self.authenticate()
            return token.is_valid()
        except RSGeAuthError:
            return False

