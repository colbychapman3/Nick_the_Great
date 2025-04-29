"""
Pinterest API authentication module.
Handles OAuth 2.0 flow, token management, and refresh.
"""

import os
import json
import time
import logging
from typing import Dict, Optional, Tuple
import requests
from urllib.parse import urlencode

from ..utils.config import get_config

logger = logging.getLogger(__name__)

class PinterestAuth:
    """Pinterest API authentication handler."""
    
    def __init__(self, token_file: Optional[str] = None):
        """
        Initialize Pinterest authentication handler.
        
        Args:
            token_file: Path to token storage file (relative to config directory)
        """
        self.config = get_config()
        
        # Set up token storage
        if token_file is None:
            config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config")
            token_file = os.path.join(config_dir, "tokens.json")
            
        self.token_file = token_file
        self.tokens = self._load_tokens()
    
    def _load_tokens(self) -> Dict:
        """
        Load tokens from file if available.
        
        Returns:
            Dict with tokens or empty dict if file not found
        """
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as f:
                    tokens = json.load(f)
                    logger.debug("Loaded tokens from file")
                    return tokens
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Failed to load tokens from file: {str(e)}")
        
        # If tokens not loaded from file, try from environment
        env_tokens = {
            "access_token": self.config.access_token,
            "refresh_token": self.config.refresh_token,
            "expires_at": 0  # Force refresh if using env tokens
        }
        
        if env_tokens["access_token"] or env_tokens["refresh_token"]:
            logger.debug("Using tokens from environment variables")
            return env_tokens
            
        return {}
    
    def _save_tokens(self) -> None:
        """Save tokens to file."""
        try:
            os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
            with open(self.token_file, 'w') as f:
                json.dump(self.tokens, f)
            logger.debug("Saved tokens to file")
        except IOError as e:
            logger.error(f"Failed to save tokens to file: {str(e)}")
    
    def get_authorization_url(self, redirect_uri: str, scope: Optional[str] = None) -> str:
        """
        Get authorization URL for OAuth flow.
        
        Args:
            redirect_uri: Redirect URI for OAuth callback
            scope: Requested permission scopes (comma-separated)
            
        Returns:
            URL to redirect user to for authorization
        """
        if scope is None:
            scope = "pins:read,pins:write,boards:read,boards:write,user_accounts:read"
            
        params = {
            "client_id": self.config.app_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scope
        }
        
        auth_url = f"https://www.pinterest.com/oauth/authorize?{urlencode(params)}"
        return auth_url
    
    def exchange_code_for_tokens(self, code: str, redirect_uri: str) -> Dict:
        """
        Exchange authorization code for tokens.
        
        Args:
            code: Authorization code from OAuth callback
            redirect_uri: Redirect URI used in authorization request
            
        Returns:
            Dict with tokens and expiration
            
        Raises:
            ValueError: If exchange fails
        """
        token_url = "https://api.pinterest.com/v5/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri
        }
        
        auth = (self.config.app_id, self.config.app_secret)
        
        try:
            response = requests.post(token_url, data=data, auth=auth)
            response.raise_for_status()
            
            token_data = response.json()
            self.tokens = {
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "expires_at": time.time() + token_data["expires_in"]
            }
            self._save_tokens()
            
            logger.info("Successfully exchanged code for tokens")
            return self.tokens
            
        except (requests.RequestException, KeyError, json.JSONDecodeError) as e:
            error_msg = f"Failed to exchange code for tokens: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def refresh_access_token(self) -> Dict:
        """
        Refresh access token using refresh token.
        
        Returns:
            Dict with new tokens and expiration
            
        Raises:
            ValueError: If refresh fails
        """
        if not self.tokens.get("refresh_token"):
            raise ValueError("No refresh token available")
            
        token_url = "https://api.pinterest.com/v5/oauth/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.tokens["refresh_token"]
        }
        
        auth = (self.config.app_id, self.config.app_secret)
        
        try:
            response = requests.post(token_url, data=data, auth=auth)
            response.raise_for_status()
            
            token_data = response.json()
            self.tokens = {
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "expires_at": time.time() + token_data["expires_in"]
            }
            self._save_tokens()
            
            logger.info("Successfully refreshed access token")
            return self.tokens
            
        except (requests.RequestException, KeyError, json.JSONDecodeError) as e:
            error_msg = f"Failed to refresh access token: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def get_access_token(self) -> str:
        """
        Get valid access token, refreshing if necessary.
        
        Returns:
            Valid access token
            
        Raises:
            ValueError: If no valid token is available
        """
        # Check if we have an access token
        if not self.tokens.get("access_token"):
            raise ValueError("No access token available. Please authorize with Pinterest first.")
            
        # Check if token is expired or about to expire (within 5 minutes)
        if self.tokens.get("expires_at", 0) < time.time() + 300:
            logger.debug("Access token expired or about to expire, refreshing")
            self.refresh_access_token()
            
        return self.tokens["access_token"]
        
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        
        Returns:
            Dict with Authorization header
            
        Raises:
            ValueError: If no valid token is available
        """
        return {
            "Authorization": f"Bearer {self.get_access_token()}"
        }
    
    def create_session(self) -> requests.Session:
        """
        Create a requests session with authentication headers.
        
        Returns:
            Session object with auth headers
            
        Raises:
            ValueError: If no valid token is available
        """
        session = requests.Session()
        session.headers.update(self.get_auth_headers())
        return session
        
    def is_authorized(self) -> bool:
        """
        Check if we have authorization credentials.
        
        Returns:
            True if we have credentials, False otherwise
        """
        try:
            self.get_access_token()
            return True
        except ValueError:
            return False
