"""
Domain interfaces defining contracts for external dependencies.
These interfaces ensure loose coupling and enable easy testing with mocks.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .models import FacebookAd, AdSearchQuery, AdSearchResult


class IFacebookAdsRepository(ABC):
    """
    Interface for Facebook Ads Library data retrieval.
    This abstraction allows us to easily swap implementations or mock for testing.
    """

    @abstractmethod
    async def search_ads(self, query: AdSearchQuery, access_token: str) -> AdSearchResult:
        """
        Search ads in Facebook Ads Library.
        
        Args:
            query: Search query parameters
            access_token: Facebook app access token (app_id|app_secret)
            
        Returns:
            AdSearchResult containing list of ads and metadata
            
        Raises:
            FacebookApiError: If API request fails
            AuthenticationError: If access token is invalid
            RateLimitExceededError: If rate limit is exceeded
        """
        pass

    @abstractmethod
    async def get_ad_by_id(self, ad_id: str, access_token: str) -> Optional[FacebookAd]:
        """
        Get specific ad by ID from Facebook Ads Library.
        
        Args:
            ad_id: Facebook ad ID
            access_token: Facebook app access token (app_id|app_secret)
            
        Returns:
            FacebookAd entity or None if not found
            
        Raises:
            FacebookApiError: If API request fails
            AuthenticationError: If access token is invalid
        """
        pass

    @abstractmethod
    async def get_next_page(self, next_page_url: str) -> AdSearchResult:
        """
        Get next page of search results using pagination URL.
        
        Args:
            next_page_url: URL for the next page from previous search result
            
        Returns:
            AdSearchResult containing next page of ads
            
        Raises:
            FacebookApiError: If API request fails
        """
        pass


class IConfigurationService(ABC):
    """
    Interface for configuration management.
    Abstracts away configuration sources (env vars, files, etc).
    """

    @abstractmethod
    def get_facebook_api_version(self) -> str:
        """Get Facebook Graph API version to use"""
        pass

    @abstractmethod
    def get_facebook_base_url(self) -> str:
        """Get Facebook Graph API base URL"""
        pass

    @abstractmethod
    def get_ads_archive_endpoint(self) -> str:
        """Get Facebook Ads Archive endpoint"""
        pass

    @abstractmethod
    def get_request_timeout(self) -> int:
        """Get HTTP request timeout in seconds"""
        pass

    @abstractmethod
    def get_facebook_app_id(self) -> str:
        """Get Facebook App ID from environment"""
        pass

    @abstractmethod
    def get_facebook_app_secret(self) -> str:
        """Get Facebook App Secret from environment"""
        pass
