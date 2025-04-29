"""
Pinterest API client module.
Handles interaction with Pinterest API endpoints.
"""

import logging
import json
from typing import Dict, List, Optional, Any, Union
import requests
from urllib.parse import urljoin

from .auth import PinterestAuth
from ..utils.config import get_config

logger = logging.getLogger(__name__)

class PinterestClient:
    """Client for interacting with Pinterest API."""
    
    def __init__(self, auth: Optional[PinterestAuth] = None):
        """
        Initialize Pinterest API client.
        
        Args:
            auth: PinterestAuth instance (creates new one if not provided)
        """
        self.config = get_config()
        self.auth = auth if auth is not None else PinterestAuth()
        self.base_url = self.config.api_url
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None, 
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        files: Optional[Dict] = None
    ) -> Dict:
        """
        Make authenticated request to Pinterest API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (relative to base URL)
            params: URL parameters
            data: Form data
            json_data: JSON data
            files: Files to upload
            
        Returns:
            API response as dict
            
        Raises:
            requests.HTTPError: If API request fails
        """
        url = urljoin(self.base_url, endpoint)
        headers = self.auth.get_auth_headers()
        
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                files=files,
                headers=headers
            )
            
            # Log details for debugging
            logger.debug(f"API Request: {method} {url}")
            logger.debug(f"Status Code: {response.status_code}")
            
            # Check for successful response
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {}
            
        except requests.HTTPError as e:
            logger.error(f"API error: {str(e)}")
            
            # Try to extract error details from response
            try:
                error_detail = response.json()
                logger.error(f"Error details: {json.dumps(error_detail)}")
            except (ValueError, AttributeError):
                logger.error(f"Response content: {response.content if hasattr(response, 'content') else 'None'}")
                
            raise
    
    # User endpoints
    
    def get_user_account(self) -> Dict:
        """
        Get authenticated user account information.
        
        Returns:
            User account data
        """
        return self._make_request("GET", "user_account")
    
    # Board endpoints
    
    def get_boards(self, page_size: int = 25, bookmark: Optional[str] = None) -> Dict:
        """
        Get user's boards.
        
        Args:
            page_size: Number of boards per page
            bookmark: Pagination bookmark
            
        Returns:
            Dict with boards and pagination info
        """
        params = {"page_size": page_size}
        if bookmark:
            params["bookmark"] = bookmark
            
        return self._make_request("GET", "boards", params=params)
    
    def create_board(
        self, 
        name: str, 
        description: Optional[str] = None, 
        privacy: str = "PUBLIC"
    ) -> Dict:
        """
        Create a new board.
        
        Args:
            name: Board name
            description: Board description
            privacy: Board privacy setting (PUBLIC or PROTECTED)
            
        Returns:
            Created board data
        """
        data = {
            "name": name,
            "privacy": privacy
        }
        
        if description:
            data["description"] = description
            
        return self._make_request("POST", "boards", json_data=data)
    
    def get_board(self, board_id: str) -> Dict:
        """
        Get board by ID.
        
        Args:
            board_id: Board ID
            
        Returns:
            Board data
        """
        return self._make_request("GET", f"boards/{board_id}")
    
    # Pin endpoints
    
    def create_pin(
        self,
        board_id: str,
        title: str,
        description: Optional[str] = None,
        link: Optional[str] = None,
        image_url: Optional[str] = None,
        image_path: Optional[str] = None,
        alt_text: Optional[str] = None
    ) -> Dict:
        """
        Create a new pin.
        
        Args:
            board_id: Board ID to pin to
            title: Pin title
            description: Pin description
            link: Destination link
            image_url: Image URL (mutually exclusive with image_path)
            image_path: Local image path (mutually exclusive with image_url)
            alt_text: Image alt text
            
        Returns:
            Created pin data
            
        Raises:
            ValueError: If neither image_url nor image_path is provided
        """
        if not image_url and not image_path:
            raise ValueError("Either image_url or image_path must be provided")
            
        data = {
            "board_id": board_id,
            "title": title
        }
        
        # Add optional fields
        if description:
            data["description"] = description
            
        if link:
            data["link"] = link
            
        if alt_text:
            data["alt_text"] = alt_text
            
        # Handle image source
        if image_url:
            data["media_source"] = {
                "source_type": "image_url",
                "url": image_url
            }
            return self._make_request("POST", "pins", json_data=data)
        else:
            # For image upload, we need to use multipart form data
            import os
            if not os.path.exists(image_path):
                raise ValueError(f"Image file not found: {image_path}")
                
            with open(image_path, 'rb') as image_file:
                files = {'image': image_file}
                data_without_media = data.copy()
                
                return self._make_request("POST", "pins", data=data_without_media, files=files)
    
    def get_pins(
        self,
        board_id: Optional[str] = None,
        page_size: int = 25,
        bookmark: Optional[str] = None
    ) -> Dict:
        """
        Get pins (all or for a specific board).
        
        Args:
            board_id: Optional board ID to filter pins
            page_size: Number of pins per page
            bookmark: Pagination bookmark
            
        Returns:
            Dict with pins and pagination info
        """
        if board_id:
            endpoint = f"boards/{board_id}/pins"
        else:
            endpoint = "pins"
            
        params = {"page_size": page_size}
        if bookmark:
            params["bookmark"] = bookmark
            
        return self._make_request("GET", endpoint, params=params)
    
    def get_pin(self, pin_id: str) -> Dict:
        """
        Get pin by ID.
        
        Args:
            pin_id: Pin ID
            
        Returns:
            Pin data
        """
        return self._make_request("GET", f"pins/{pin_id}")
    
    def delete_pin(self, pin_id: str) -> None:
        """
        Delete pin by ID.
        
        Args:
            pin_id: Pin ID
        """
        self._make_request("DELETE", f"pins/{pin_id}")
        logger.info(f"Deleted pin {pin_id}")
    
    # Analytics endpoints
    
    def get_pin_analytics(
        self,
        pin_id: str,
        start_date: str,
        end_date: str,
        metrics: Optional[List[str]] = None
    ) -> Dict:
        """
        Get analytics for a specific pin.
        
        Args:
            pin_id: Pin ID
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            metrics: List of metrics to retrieve (defaults to all)
            
        Returns:
            Pin analytics data
        """
        if not metrics:
            metrics = ["IMPRESSION", "SAVE", "PIN_CLICK", "OUTBOUND_CLICK"]
            
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "metric_types": ",".join(metrics)
        }
        
        return self._make_request("GET", f"pins/{pin_id}/analytics", params=params)
    
    def get_board_analytics(
        self,
        board_id: str,
        start_date: str,
        end_date: str,
        metrics: Optional[List[str]] = None
    ) -> Dict:
        """
        Get analytics for a specific board.
        
        Args:
            board_id: Board ID
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            metrics: List of metrics to retrieve (defaults to all)
            
        Returns:
            Board analytics data
        """
        if not metrics:
            metrics = ["IMPRESSION", "SAVE", "PIN_CLICK", "OUTBOUND_CLICK"]
            
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "metric_types": ",".join(metrics)
        }
        
        return self._make_request("GET", f"boards/{board_id}/analytics", params=params)
    
    def get_user_analytics(
        self,
        start_date: str,
        end_date: str,
        metrics: Optional[List[str]] = None
    ) -> Dict:
        """
        Get analytics for the authenticated user.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            metrics: List of metrics to retrieve (defaults to all)
            
        Returns:
            User analytics data
        """
        if not metrics:
            metrics = ["IMPRESSION", "SAVE", "PIN_CLICK", "OUTBOUND_CLICK", "ENGAGEMENT"]
            
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "metric_types": ",".join(metrics)
        }
        
        return self._make_request("GET", "user_account/analytics", params=params)
