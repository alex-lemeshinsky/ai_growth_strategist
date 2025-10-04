"""
Configuration service implementation.
Handles loading configuration from environment variables and provides defaults.
"""

import os
from typing import Optional
from dotenv import load_dotenv

from domain.interfaces import IConfigurationService
from domain.exceptions import FacebookDomainError


class ConfigurationService(IConfigurationService):
    """
    Concrete implementation of configuration service.
    Loads configuration from environment variables.
    """
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration service.
        
        Args:
            env_file: Optional path to .env file. If None, will look in current directory.
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
    
    def get_facebook_api_version(self) -> str:
        """Get Facebook Graph API version to use"""
        return os.getenv('FB_API_VERSION', 'v23.0')
    
    def get_facebook_base_url(self) -> str:
        """Get Facebook Graph API base URL"""
        return os.getenv('FB_BASE_URL', 'https://graph.facebook.com')
    
    def get_ads_archive_endpoint(self) -> str:
        """Get Facebook Ads Archive endpoint"""
        return os.getenv('FB_ADS_ARCHIVE_ENDPOINT', 'ads_archive')
    
    def get_request_timeout(self) -> int:
        """Get HTTP request timeout in seconds"""
        timeout_str = os.getenv('REQUEST_TIMEOUT', '30')
        try:
            return int(timeout_str)
        except ValueError:
            return 30
    
    def get_facebook_app_id(self) -> str:
        """Get Facebook App ID from environment"""
        app_id = os.getenv('FB_APP_ID')
        if not app_id:
            raise FacebookDomainError(
                "FB_APP_ID environment variable is required. "
                "Please set it in your .env file or environment."
            )
        return app_id
    
    def get_facebook_app_secret(self) -> str:
        """Get Facebook App Secret from environment"""
        app_secret = os.getenv('FB_APP_SECRET')
        if not app_secret:
            raise FacebookDomainError(
                "FB_APP_SECRET environment variable is required. "
                "Please set it in your .env file or environment."
            )
        return app_secret

    def get_facebook_user_secret(self) -> str:
        user_secret = os.getenv("FB_USER_ACCESS_TOKEN")
        if not user_secret:
            raise FacebookDomainError(
                "FB_USER_ACCESS_TOKEN environment variable is required. "
                "Please set it in your .env file or environment."
            )
        return user_secret
    
    def get_facebook_user_access_token(self) -> str:
        """Get Facebook User Access Token from environment"""
        user_token = os.getenv('FB_USER_ACCESS_TOKEN')
        if not user_token:
            raise FacebookDomainError(
                "FB_USER_ACCESS_TOKEN environment variable is required. "
                "Please set it in your .env file or environment."
            )
        return user_token
    
    def get_access_token(self) -> str:
        """Get access token - prefer user token over app token"""
        try:
            return self.get_facebook_user_access_token()
        except FacebookDomainError:
            # Fallback to app token if user token not available
            try:
                app_id = self.get_facebook_app_id()
                app_secret = self.get_facebook_app_secret()
                return f"{app_id}|{app_secret}"
            except FacebookDomainError:
                raise FacebookDomainError(
                    "No valid access token found. Please set either FB_USER_ACCESS_TOKEN "
                    "or both FB_APP_ID and FB_APP_SECRET in your .env file."
                )
