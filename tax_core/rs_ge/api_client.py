"""RS.ge API client for fetching taxpayer data."""
import requests
from typing import List, Dict, Optional
from datetime import datetime
from tax_core.rs_ge.auth import RSGeAuth, AuthToken
from tax_core.rs_ge.exceptions import (
    RSGeAPIError,
    RSGeConnectionError,
    RSGeRateLimitError,
)


class RSGeAPIClient:
    """Client for interacting with RS.ge API."""
    
    # RS.ge API base URL (to be updated with actual endpoints)
    BASE_URL = "https://services.rs.ge/api"  # Placeholder
    
    def __init__(self, auth: Optional[RSGeAuth] = None):
        """
        Initialize RS.ge API client.
        
        Args:
            auth: RS.ge authentication instance (creates new if not provided)
        """
        self.auth = auth or RSGeAuth()
        self._session = requests.Session()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token."""
        token = self.auth.get_token()
        return {
            "Authorization": f"{token.token_type} {token.token}",
            "Content-Type": "application/json",
        }
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Dict:
        """
        Make API request to RS.ge.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON request body
            
        Returns:
            Dict: API response data
            
        Raises:
            RSGeAPIError: If API request fails
            RSGeConnectionError: If connection fails
            RSGeRateLimitError: If rate limit exceeded
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        
        try:
            response = self._session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                timeout=30,
            )
            
            if response.status_code == 429:
                raise RSGeRateLimitError("RS.ge API rate limit exceeded")
            elif response.status_code == 401:
                # Token expired, try to refresh
                self.auth.refresh_token()
                headers = self._get_headers()
                response = self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json_data,
                    timeout=30,
                )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError as e:
            raise RSGeConnectionError(f"Failed to connect to RS.ge: {str(e)}")
        except requests.exceptions.Timeout as e:
            raise RSGeConnectionError(f"Request to RS.ge timed out: {str(e)}")
        except requests.exceptions.HTTPError as e:
            raise RSGeAPIError(f"RS.ge API error: {response.status_code} - {str(e)}")
        except Exception as e:
            raise RSGeAPIError(f"Unexpected error: {str(e)}")
    
    def get_income_declarations(self, year: int) -> List[Dict]:
        """
        Get income declarations for a specific year.
        
        Args:
            year: Tax year
            
        Returns:
            List[Dict]: List of income declaration records
        """
        # TODO: Implement actual endpoint when RS.ge API documentation is available
        endpoint = f"income/declarations/{year}"
        response = self._make_request("GET", endpoint)
        return response.get("data", [])
    
    def get_tax_payments(self, year: int) -> List[Dict]:
        """
        Get tax payment history for a specific year.
        
        Args:
            year: Tax year
            
        Returns:
            List[Dict]: List of tax payment records
        """
        # TODO: Implement actual endpoint
        endpoint = f"tax/payments/{year}"
        response = self._make_request("GET", endpoint)
        return response.get("data", [])
    
    def get_property_info(self) -> List[Dict]:
        """
        Get registered property information.
        
        Returns:
            List[Dict]: List of property records
        """
        # TODO: Implement actual endpoint
        endpoint = "property/info"
        response = self._make_request("GET", endpoint)
        return response.get("data", [])
    
    def get_business_info(self) -> Dict:
        """
        Get business registration information.
        
        Returns:
            Dict: Business registration data
        """
        # TODO: Implement actual endpoint
        endpoint = "business/info"
        response = self._make_request("GET", endpoint)
        return response.get("data", {})
    
    def get_taxpayer_profile(self) -> Dict:
        """
        Get basic taxpayer profile information.
        
        Returns:
            Dict: Taxpayer profile data
        """
        # TODO: Implement actual endpoint
        endpoint = "taxpayer/profile"
        response = self._make_request("GET", endpoint)
        return response.get("data", {})

