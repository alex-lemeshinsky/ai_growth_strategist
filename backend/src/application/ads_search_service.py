"""
Application layer use cases for Facebook Ads Library operations.
Contains business logic and orchestrates domain models and infrastructure.
"""

from typing import List, Optional
from domain.interfaces import IFacebookAdsRepository, IConfigurationService
from domain.models import FacebookAd, AdSearchQuery, AdSearchResult, AdActiveStatus
from domain.exceptions import InvalidSearchQueryError


class AdsSearchService:
    """
    Use case service for searching and retrieving Facebook ads.
    This is the main business logic layer that coordinates between domain and infrastructure.
    """
    
    def __init__(self, ads_repository: IFacebookAdsRepository, config_service: IConfigurationService):
        self.ads_repository = ads_repository
        self.config = config_service
    
    async def search_ads(
        self, 
        search_terms: str, 
        country: str = "US", 
        limit: int = 20, 
        active_status: AdActiveStatus = AdActiveStatus.ALL
    ) -> AdSearchResult:
        """
        Search for ads in Facebook Ads Library.
        
        Args:
            search_terms: Keywords to search for in ad content
            country: Country code (US, UA, GB, etc.)
            limit: Maximum number of results to return (1-100)
            active_status: Filter by ad status (ALL, ACTIVE, INACTIVE)
            
        Returns:
            AdSearchResult containing matching ads and pagination info
            
        Raises:
            InvalidSearchQueryError: If search parameters are invalid
            FacebookApiError: If API request fails
            AuthenticationError: If credentials are invalid
        """
        # Validate input
        if not search_terms or not search_terms.strip():
            raise InvalidSearchQueryError("Search terms cannot be empty")
        
        if limit < 1 or limit > 100:
            raise InvalidSearchQueryError("Limit must be between 1 and 100")
        
        if len(country) != 2:
            raise InvalidSearchQueryError("Country code must be 2 characters (e.g., 'US', 'UA')")
        
        # Create search query
        query = AdSearchQuery(
            search_terms=search_terms.strip(),
            ad_reached_countries=country.upper(),
            limit=limit,
            ad_active_status=active_status
        )
        
        # Get access token and execute search
        access_token = self.config.get_access_token()
        return await self.ads_repository.search_ads(query, access_token)
    
    async def get_next_page(self, next_page_url: str) -> AdSearchResult:
        """
        Get next page of search results.
        
        Args:
            next_page_url: Pagination URL from previous search result
            
        Returns:
            AdSearchResult containing next page of ads
            
        Raises:
            FacebookApiError: If API request fails
        """
        if not next_page_url:
            raise InvalidSearchQueryError("Next page URL cannot be empty")
        
        return await self.ads_repository.get_next_page(next_page_url)
    
    async def get_competitor_ads(
        self, 
        competitor_keywords: List[str], 
        country: str = "US", 
        limit_per_keyword: int = 10
    ) -> List[AdSearchResult]:
        """
        Search for competitor ads using multiple keywords.
        
        Args:
            competitor_keywords: List of keywords related to competitors
            country: Country code to search in
            limit_per_keyword: Number of results per keyword
            
        Returns:
            List of AdSearchResult, one for each keyword
            
        Raises:
            InvalidSearchQueryError: If parameters are invalid
            FacebookApiError: If any API request fails
        """
        if not competitor_keywords:
            raise InvalidSearchQueryError("At least one keyword is required")
        
        results = []
        for keyword in competitor_keywords:
            if keyword.strip():  # Skip empty keywords
                result = await self.search_ads(
                    search_terms=keyword,
                    country=country,
                    limit=limit_per_keyword,
                    active_status=AdActiveStatus.ACTIVE  # Only active competitor ads
                )
                results.append(result)
        
        return results
    
    async def search_by_page_name(self, page_name: str, country: str = "US", limit: int = 20) -> AdSearchResult:
        """
        Search for ads from a specific Facebook page.
        
        Args:
            page_name: Name of the Facebook page to search for
            country: Country code to search in
            limit: Maximum number of results
            
        Returns:
            AdSearchResult containing ads from the specified page
            
        Note:
            This uses page name as search term. Facebook Ads Library doesn't have
            direct page filtering, so results may include ads that mention the page name
            rather than ads only from that page.
        """
        return await self.search_ads(
            search_terms=page_name,
            country=country,
            limit=limit,
            active_status=AdActiveStatus.ALL
        )
    
    def filter_ads_by_platform(self, ads: List[FacebookAd], platforms: List[str]) -> List[FacebookAd]:
        """
        Filter ads by publisher platforms.
        
        Args:
            ads: List of ads to filter
            platforms: List of platform names ('facebook', 'instagram', etc.)
            
        Returns:
            Filtered list of ads that run on specified platforms
        """
        filtered_ads = []
        platform_set = set(platforms)
        
        for ad in ads:
            ad_platforms = {platform.value for platform in ad.publisher_platforms}
            if platform_set.intersection(ad_platforms):
                filtered_ads.append(ad)
        
        return filtered_ads
    
    def get_ads_summary(self, search_result: AdSearchResult) -> dict:
        """
        Generate summary statistics for search results.
        
        Args:
            search_result: Result from ads search
            
        Returns:
            Dictionary containing summary statistics
        """
        ads = search_result.ads
        
        if not ads:
            return {
                'total_ads': 0,
                'active_ads': 0,
                'platforms': {},
                'pages': {},
                'has_more_pages': search_result.has_more_pages
            }
        
        # Count active ads
        active_ads = sum(1 for ad in ads if ad.is_active)
        
        # Count ads by platform
        platform_counts = {}
        for ad in ads:
            for platform in ad.publisher_platforms:
                platform_counts[platform.value] = platform_counts.get(platform.value, 0) + 1
        
        # Count ads by page
        page_counts = {}
        for ad in ads:
            if ad.page_name:
                page_counts[ad.page_name] = page_counts.get(ad.page_name, 0) + 1
        
        return {
            'total_ads': len(ads),
            'active_ads': active_ads,
            'platforms': platform_counts,
            'top_pages': dict(sorted(page_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            'has_more_pages': search_result.has_more_pages
        }
    
    async def close(self):
        """Close repository connections"""
        if hasattr(self.ads_repository, 'close'):
            await self.ads_repository.close()