"""
Unit tests for FacebookAdsRepository.
Uses mocks to test HTTP client behavior without actual API calls.
"""

import pytest
from unittest.mock import Mock, AsyncMock, MagicMock
from datetime import datetime
import json

from src.infrastructure.facebook_ads_repository import FacebookAdsRepository
from src.domain.models import AdSearchQuery, AdActiveStatus, FacebookAd, PublisherPlatform
from src.domain.exceptions import (
    FacebookApiError, AuthenticationError, InvalidSearchQueryError, 
    RateLimitExceededError
)


class TestFacebookAdsRepository:
    """Tests for FacebookAdsRepository infrastructure layer"""
    
    def setup_method(self):
        """Set up test dependencies"""
        self.mock_config = Mock()
        
        # Configure mock config
        self.mock_config.get_facebook_base_url.return_value = "https://graph.facebook.com"
        self.mock_config.get_facebook_api_version.return_value = "v21.0"
        self.mock_config.get_ads_archive_endpoint.return_value = "ads_archive"
        self.mock_config.get_request_timeout.return_value = 30
        
        # Create repository
        self.repository = FacebookAdsRepository(self.mock_config)
        
        # Mock aiohttp session
        self.mock_session = Mock()
        self.repository._session = self.mock_session
    
    def create_sample_api_response(self) -> dict:
        """Create sample API response data"""
        return {
            "data": [
                {
                    "id": "123456789",
                    "page_name": "Test Page",
                    "page_id": "987654321",
                    "ad_creation_time": "2024-01-01T12:00:00Z",
                    "ad_delivery_start_time": "2024-01-01T12:00:00Z",
                    "ad_delivery_stop_time": None,
                    "ad_snapshot_url": "https://facebook.com/ads/snapshot/123456789",
                    "currency": "USD",
                    "ad_creative_bodies": ["Test ad body"],
                    "ad_creative_link_titles": ["Test Title"],
                    "ad_creative_link_descriptions": ["Test description"],
                    "ad_creative_link_captions": ["Test caption"],
                    "publisher_platforms": ["facebook", "instagram"],
                    "impressions": {"lower_bound": 1000, "upper_bound": 5000},
                    "spend": {"lower_bound": 100, "upper_bound": 500}
                }
            ],
            "paging": {
                "next": "https://graph.facebook.com/v21.0/ads_archive?next_page_token=abc123"
            }
        }
    
    def test_build_ads_archive_url(self):
        """Test URL building for ads archive endpoint"""
        url = self.repository._build_ads_archive_url()
        assert url == "https://graph.facebook.com/v21.0/ads_archive"
    
    def test_build_query_params(self):
        """Test query parameter building"""
        query = AdSearchQuery(
            search_terms="fitness",
            ad_reached_countries="US",
            limit=10,
            ad_active_status=AdActiveStatus.ACTIVE
        )
        
        params = self.repository._build_query_params(query, "test_token")
        
        assert params["access_token"] == "test_token"
        assert params["search_terms"] == "fitness"
        assert params["ad_reached_countries"] == "US"
        assert params["limit"] == 10
        assert params["ad_active_status"] == "ACTIVE"
        assert "fields" in params
        assert "id" in params["fields"]
        assert "page_name" in params["fields"]
    
    def test_build_query_params_limits_to_100(self):
        """Test that limit is capped at 100 per Facebook API rules"""
        query = AdSearchQuery(search_terms="fitness", limit=150)
        params = self.repository._build_query_params(query, "token")
        assert params["limit"] == 100
    
    def test_parse_datetime_valid(self):
        """Test datetime parsing from API response"""
        date_string = "2024-01-01T12:00:00Z"
        parsed = self.repository._parse_datetime(date_string)
        
        assert isinstance(parsed, datetime)
        assert parsed.year == 2024
        assert parsed.month == 1
        assert parsed.day == 1
    
    def test_parse_datetime_none(self):
        """Test datetime parsing with None input"""
        assert self.repository._parse_datetime(None) is None
    
    def test_parse_datetime_invalid(self):
        """Test datetime parsing with invalid input"""
        assert self.repository._parse_datetime("invalid") is None
    
    def test_parse_spend_range(self):
        """Test spend range parsing"""
        spend_data = {"lower_bound": 100, "upper_bound": 500}
        spend_range = self.repository._parse_spend_range(spend_data)
        
        assert spend_range.lower_bound == 100
        assert spend_range.upper_bound == 500
    
    def test_parse_spend_range_none(self):
        """Test spend range parsing with None"""
        assert self.repository._parse_spend_range(None) is None
    
    def test_parse_impression_range(self):
        """Test impression range parsing"""
        impression_data = {"lower_bound": 1000, "upper_bound": 5000}
        impression_range = self.repository._parse_impression_range(impression_data)
        
        assert impression_range.lower_bound == 1000
        assert impression_range.upper_bound == 5000
    
    def test_parse_platforms(self):
        """Test platform parsing from strings to enums"""
        platforms = ["facebook", "instagram", "unknown_platform"]
        parsed = self.repository._parse_platforms(platforms)
        
        assert len(parsed) == 2  # unknown_platform should be skipped
        assert PublisherPlatform.FACEBOOK in parsed
        assert PublisherPlatform.INSTAGRAM in parsed
    
    def test_parse_platforms_empty(self):
        """Test platform parsing with empty list"""
        assert self.repository._parse_platforms([]) == []
        assert self.repository._parse_platforms(None) == []
    
    def test_parse_ad_data(self):
        """Test parsing complete ad data from API response"""
        api_data = self.create_sample_api_response()["data"][0]
        ad = self.repository._parse_ad_data(api_data)
        
        assert isinstance(ad, FacebookAd)
        assert ad.id == "123456789"
        assert ad.page_name == "Test Page"
        assert ad.primary_text == "Test ad body"
        assert ad.primary_title == "Test Title"
        assert len(ad.publisher_platforms) == 2
        assert ad.currency == "USD"
        assert ad.spend.lower_bound == 100
        assert ad.impressions.lower_bound == 1000
    
    @pytest.mark.asyncio
    async def test_search_ads_success(self):
        \"\"\"Test successful ad search\"\"\"
        # Mock HTTP response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json = AsyncMock(return_value=self.create_sample_api_response())
        
        # Mock session.get context manager
        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        self.mock_session.get.return_value = mock_context
        
        # Execute search
        query = AdSearchQuery(search_terms="fitness")
        result = await self.repository.search_ads(query, "test_token")
        
        # Verify result
        assert len(result.ads) == 1
        assert result.ads[0].id == "123456789"
        assert result.next_page_url is not None
        
        # Verify HTTP call was made
        self.mock_session.get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_search_ads_empty_search_terms(self):
        \"\"\"Test search with empty search terms raises error\"\"\"
        query = AdSearchQuery(search_terms="")
        
        with pytest.raises(InvalidSearchQueryError, match="Search terms cannot be empty"):
            await self.repository.search_ads(query, "test_token")
    
    @pytest.mark.asyncio
    async def test_search_ads_api_error_401(self):
        \"\"\"Test handling of 401 authentication error\"\"\"
        # Mock HTTP error response
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status = 401
        mock_response.json = AsyncMock(return_value={
            "error": {"message": "Invalid access token", "code": 190}
        })
        
        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        self.mock_session.get.return_value = mock_context
        
        query = AdSearchQuery(search_terms="fitness")
        
        with pytest.raises(AuthenticationError, match="Authentication failed"):
            await self.repository.search_ads(query, "test_token")
    
    @pytest.mark.asyncio
    async def test_search_ads_api_error_429(self):
        \"\"\"Test handling of 429 rate limit error\"\"\"
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status = 429
        mock_response.json = AsyncMock(return_value={
            "error": {"message": "Rate limit exceeded", "code": 4}
        })
        
        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        self.mock_session.get.return_value = mock_context
        
        query = AdSearchQuery(search_terms="fitness")
        
        with pytest.raises(RateLimitExceededError):
            await self.repository.search_ads(query, "test_token")
    
    @pytest.mark.asyncio
    async def test_search_ads_api_error_400_search_terms(self):
        \"\"\"Test handling of 400 error for invalid search terms\"\"\"
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status = 400
        mock_response.json = AsyncMock(return_value={
            "error": {"message": "Invalid search_terms parameter", "code": 100}
        })
        
        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        self.mock_session.get.return_value = mock_context
        
        query = AdSearchQuery(search_terms="fitness")
        
        with pytest.raises(InvalidSearchQueryError):
            await self.repository.search_ads(query, "test_token")
    
    @pytest.mark.asyncio
    async def test_search_ads_generic_api_error(self):
        \"\"\"Test handling of generic API error\"\"\"
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status = 500
        mock_response.json = AsyncMock(return_value={
            "error": {"message": "Internal server error", "code": 1}
        })
        
        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        self.mock_session.get.return_value = mock_context
        
        query = AdSearchQuery(search_terms="fitness")
        
        with pytest.raises(FacebookApiError) as exc_info:
            await self.repository.search_ads(query, "test_token")
        
        assert exc_info.value.http_status == 500
        assert exc_info.value.error_code == "1"
    
    @pytest.mark.asyncio
    async def test_get_next_page_success(self):
        \"\"\"Test successful next page retrieval\"\"\"
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json = AsyncMock(return_value=self.create_sample_api_response())
        
        mock_context = AsyncMock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_context.__aexit__ = AsyncMock(return_value=None)
        self.mock_session.get.return_value = mock_context
        
        result = await self.repository.get_next_page("https://example.com/next")
        
        assert len(result.ads) == 1
        self.mock_session.get.assert_called_once_with("https://example.com/next")
    
    @pytest.mark.asyncio
    async def test_get_ad_by_id_not_implemented(self):
        \"\"\"Test that get_ad_by_id returns None (not implemented)\"\"\"
        result = await self.repository.get_ad_by_id("123", "token")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_close(self):
        \"\"\"Test repository close functionality\"\"\"
        self.mock_session.close = AsyncMock()
        
        await self.repository.close()
        
        self.mock_session.close.assert_called_once()
        assert self.repository._session is None
    
    @pytest.mark.asyncio
    async def test_get_session_creates_new_session(self):
        \"\"\"Test that _get_session creates a new session when needed\"\"\"
        # Reset session to None
        self.repository._session = None
        
        # Mock aiohttp.ClientSession
        with pytest.MonkeyPatch().context() as m:
            mock_session_class = Mock()
            mock_session_instance = Mock()
            mock_session_class.return_value = mock_session_instance
            m.setattr("aiohttp.ClientSession", mock_session_class)
            
            session = await self.repository._get_session()
            
            assert session == mock_session_instance
            assert self.repository._session == mock_session_instance