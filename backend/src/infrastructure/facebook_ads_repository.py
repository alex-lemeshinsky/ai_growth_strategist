"""
Infrastructure implementation for Facebook Ads Library API.
This layer handles the actual HTTP communication with Facebook's API.
"""

import asyncio
import aiohttp
from datetime import datetime
from typing import Optional, Dict, Any
from urllib.parse import urlencode

from domain.interfaces import IFacebookAdsRepository, IConfigurationService
from domain.models import (
    FacebookAd, AdSearchQuery, AdSearchResult, AdSpendRange, 
    AdImpressionRange, PublisherPlatform
)
from domain.exceptions import (
    FacebookApiError, AuthenticationError, AdNotFoundError, 
    RateLimitExceededError, InvalidSearchQueryError
)


class FacebookAdsRepository(IFacebookAdsRepository):
    """
    Concrete implementation of Facebook Ads Library repository.
    Handles HTTP requests to Facebook Graph API.
    """
    
    def __init__(self, config_service: IConfigurationService):
        self.config = config_service
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if self._session is None:
            timeout = aiohttp.ClientTimeout(total=self.config.get_request_timeout())
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session
    
    async def close(self):
        """Close HTTP session"""
        if self._session:
            await self._session.close()
            self._session = None
    
    def _build_ads_archive_url(self) -> str:
        """Build full URL for ads archive endpoint"""
        base_url = self.config.get_facebook_base_url()
        api_version = self.config.get_facebook_api_version()
        endpoint = self.config.get_ads_archive_endpoint()
        return f"{base_url}/{api_version}/{endpoint}"
    
    def _build_query_params(self, query: AdSearchQuery, access_token: str) -> Dict[str, Any]:
        """Build query parameters for API request"""
        fields = [
            'id', 'ad_creation_time', 'ad_creative_bodies', 
            'ad_creative_link_captions', 'ad_creative_link_descriptions',
            'ad_creative_link_titles', 'ad_delivery_start_time',
            'ad_delivery_stop_time', 'ad_snapshot_url', 'page_name',
            'page_id', 'publisher_platforms', 'impressions', 'spend', 'currency'
        ]
        
        return {
            'access_token': access_token,
            'search_terms': query.search_terms,
            'ad_reached_countries': query.ad_reached_countries,
            'ad_active_status': query.ad_active_status.value,
            'limit': min(query.limit, 100),  # Facebook API limit
            'fields': ','.join(fields)
        }
    
    def _parse_datetime(self, date_string: Optional[str]) -> Optional[datetime]:
        """Parse Facebook API date string to datetime"""
        if not date_string:
            return None
        try:
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    
    def _parse_spend_range(self, spend_data: Optional[Dict]) -> Optional[AdSpendRange]:
        """Parse spend range from API response"""
        if not spend_data:
            return None
        return AdSpendRange(
            lower_bound=spend_data.get('lower_bound'),
            upper_bound=spend_data.get('upper_bound')
        )
    
    def _parse_impression_range(self, impression_data: Optional[Dict]) -> Optional[AdImpressionRange]:
        """Parse impression range from API response"""
        if not impression_data:
            return None
        return AdImpressionRange(
            lower_bound=impression_data.get('lower_bound'),
            upper_bound=impression_data.get('upper_bound')
        )
    
    def _parse_platforms(self, platforms: Optional[list]) -> list[PublisherPlatform]:
        """Parse publisher platforms from API response"""
        if not platforms:
            return []
        
        parsed_platforms = []
        for platform in platforms:
            try:
                parsed_platforms.append(PublisherPlatform(platform))
            except ValueError:
                # Skip unknown platforms
                continue
        return parsed_platforms
    
    def _parse_ad_data(self, ad_data: Dict[str, Any]) -> FacebookAd:
        """Parse single ad data from API response to domain model"""
        return FacebookAd(
            id=ad_data['id'],
            page_name=ad_data.get('page_name'),
            page_id=ad_data.get('page_id'),
            ad_creation_time=self._parse_datetime(ad_data.get('ad_creation_time')),
            ad_delivery_start_time=self._parse_datetime(ad_data.get('ad_delivery_start_time')),
            ad_delivery_stop_time=self._parse_datetime(ad_data.get('ad_delivery_stop_time')),
            ad_snapshot_url=ad_data.get('ad_snapshot_url'),
            currency=ad_data.get('currency'),
            ad_creative_bodies=ad_data.get('ad_creative_bodies', []),
            ad_creative_link_titles=ad_data.get('ad_creative_link_titles', []),
            ad_creative_link_descriptions=ad_data.get('ad_creative_link_descriptions', []),
            ad_creative_link_captions=ad_data.get('ad_creative_link_captions', []),
            publisher_platforms=self._parse_platforms(ad_data.get('publisher_platforms', [])),
            impressions=self._parse_impression_range(ad_data.get('impressions')),
            spend=self._parse_spend_range(ad_data.get('spend'))
        )
    
    async def _handle_api_error(self, response: aiohttp.ClientResponse, response_data: Dict):
        """Handle API error responses"""
        error_info = response_data.get('error', {})
        error_code = error_info.get('code')
        error_message = error_info.get('message', 'Unknown Facebook API error')
        
        # Handle specific error types
        if response.status == 401:
            raise AuthenticationError(f"Authentication failed: {error_message}")
        elif response.status == 429:
            raise RateLimitExceededError()
        elif response.status == 400:
            if 'search_terms' in error_message.lower():
                raise InvalidSearchQueryError(error_message)
        
        raise FacebookApiError(
            message=error_message,
            error_code=str(error_code) if error_code else None,
            http_status=response.status
        )
    
    async def search_ads(self, query: AdSearchQuery, access_token: str) -> AdSearchResult:
        """Search ads in Facebook Ads Library"""
        if not query.search_terms.strip():
            raise InvalidSearchQueryError("Search terms cannot be empty")
        
        session = await self._get_session()
        url = self._build_ads_archive_url()
        params = self._build_query_params(query, access_token)
        
        try:
            async with session.get(url, params=params) as response:
                response_data = await response.json()
                
                if not response.ok:
                    await self._handle_api_error(response, response_data)
                
                ads_data = response_data.get('data', [])
                paging = response_data.get('paging', {})
                
                ads = [self._parse_ad_data(ad) for ad in ads_data]
                
                return AdSearchResult(
                    ads=ads,
                    total_count=len(ads),
                    next_page_url=paging.get('next')
                )
                
        except aiohttp.ClientError as e:
            raise FacebookApiError(f"Network error: {str(e)}")
    
    async def get_ad_by_id(self, ad_id: str, access_token: str) -> Optional[FacebookAd]:
        """Get specific ad by ID (not directly supported by Ads Library API)"""
        # Facebook Ads Library API doesn't support direct ad lookup by ID
        # This would require searching and filtering, which is not efficient
        # For now, we return None - this could be implemented as a search operation
        return None
    
    async def get_next_page(self, next_page_url: str) -> AdSearchResult:
        """Get next page of results using pagination URL"""
        session = await self._get_session()
        
        try:
            async with session.get(next_page_url) as response:
                response_data = await response.json()
                
                if not response.ok:
                    await self._handle_api_error(response, response_data)
                
                ads_data = response_data.get('data', [])
                paging = response_data.get('paging', {})
                
                ads = [self._parse_ad_data(ad) for ad in ads_data]
                
                return AdSearchResult(
                    ads=ads,
                    total_count=len(ads),
                    next_page_url=paging.get('next')
                )
                
        except aiohttp.ClientError as e:
            raise FacebookApiError(f"Network error: {str(e)}")