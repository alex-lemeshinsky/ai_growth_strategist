"""
Unit tests for AdsSearchService.
Uses mocks to test business logic without external dependencies.
"""

import pytest
from unittest.mock import Mock, AsyncMock

from src.application.ads_search_service import AdsSearchService
from src.domain.models import (
    FacebookAd, AdSearchQuery, AdSearchResult, AdActiveStatus, PublisherPlatform
)
from src.domain.exceptions import InvalidSearchQueryError, FacebookApiError


class TestAdsSearchService:
    """Tests for AdsSearchService application layer"""
    
    def setup_method(self):
        """Set up test dependencies"""
        self.mock_repository = Mock()
        self.mock_config = Mock()
        
        # Configure mock config
        self.mock_config.get_access_token.return_value = "test_app_id|test_app_secret"
        
        # Create service
        self.service = AdsSearchService(self.mock_repository, self.mock_config)
    
    def create_sample_ad(self, ad_id: str = "123") -> FacebookAd:
        """Create a sample ad for testing"""
        return FacebookAd(
            id=ad_id,
            page_name="Test Page",
            ad_creative_bodies=["Test ad body"],
            ad_creative_link_titles=["Test Title"],
            publisher_platforms=[PublisherPlatform.FACEBOOK]
        )
    
    @pytest.mark.asyncio
    async def test_search_ads_success(self):
        """Test successful ad search"""
        # Arrange
        expected_ads = [self.create_sample_ad()]
        expected_result = AdSearchResult(ads=expected_ads, total_count=1)
        
        self.mock_repository.search_ads = AsyncMock(return_value=expected_result)
        
        # Act
        result = await self.service.search_ads(
            search_terms="fitness",
            country="US",
            limit=10
        )
        
        # Assert
        assert result == expected_result
        self.mock_repository.search_ads.assert_called_once()
        self.mock_config.get_access_token.assert_called_once()
        
        # Verify query parameters
        call_args = self.mock_repository.search_ads.call_args
        query = call_args[0][0]  # First argument is the query
        access_token = call_args[0][1]  # Second argument is access token
        
        assert query.search_terms == "fitness"
        assert query.ad_reached_countries == "US"
        assert query.limit == 10
        assert query.ad_active_status == AdActiveStatus.ALL
        assert access_token == "test_app_id|test_app_secret"
    
    @pytest.mark.asyncio
    async def test_search_ads_empty_search_terms(self):
        """Test search with empty search terms raises error"""
        with pytest.raises(InvalidSearchQueryError, match="Search terms cannot be empty"):
            await self.service.search_ads(search_terms="")
        
        # Repository should not be called
        self.mock_repository.search_ads.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_search_ads_invalid_limit(self):
        """Test search with invalid limit raises error"""
        with pytest.raises(InvalidSearchQueryError, match="Limit must be between 1 and 100"):
            await self.service.search_ads(search_terms="fitness", limit=0)
        
        with pytest.raises(InvalidSearchQueryError, match="Limit must be between 1 and 100"):
            await self.service.search_ads(search_terms="fitness", limit=101)
    
    @pytest.mark.asyncio
    async def test_search_ads_invalid_country_code(self):
        """Test search with invalid country code raises error"""
        with pytest.raises(InvalidSearchQueryError, match="Country code must be 2 characters"):
            await self.service.search_ads(search_terms="fitness", country="USA")
    
    @pytest.mark.asyncio
    async def test_search_ads_strips_whitespace(self):
        """Test that search terms are stripped of whitespace"""
        expected_result = AdSearchResult(ads=[], total_count=0)
        self.mock_repository.search_ads = AsyncMock(return_value=expected_result)
        
        await self.service.search_ads(search_terms="  fitness  ")
        
        # Verify the query had stripped search terms
        call_args = self.mock_repository.search_ads.call_args
        query = call_args[0][0]
        assert query.search_terms == "fitness"
    
    @pytest.mark.asyncio
    async def test_get_next_page_success(self):
        """Test successful next page retrieval"""
        expected_result = AdSearchResult(ads=[], total_count=0)
        self.mock_repository.get_next_page = AsyncMock(return_value=expected_result)
        
        result = await self.service.get_next_page("https://example.com/next")
        
        assert result == expected_result
        self.mock_repository.get_next_page.assert_called_once_with("https://example.com/next")
    
    @pytest.mark.asyncio
    async def test_get_next_page_empty_url(self):
        """Test next page with empty URL raises error"""
        with pytest.raises(InvalidSearchQueryError, match="Next page URL cannot be empty"):
            await self.service.get_next_page("")
    
    @pytest.mark.asyncio
    async def test_get_competitor_ads_success(self):
        """Test successful competitor analysis"""
        keywords = ["fitness app", "workout tracker"]
        
        # Mock repository to return different results for each keyword
        self.mock_repository.search_ads = AsyncMock(
            side_effect=[
                AdSearchResult(ads=[self.create_sample_ad("1")], total_count=1),
                AdSearchResult(ads=[self.create_sample_ad("2")], total_count=1)
            ]
        )
        
        results = await self.service.get_competitor_ads(keywords, limit_per_keyword=5)
        
        assert len(results) == 2
        assert self.mock_repository.search_ads.call_count == 2
        
        # Verify each call used ACTIVE status for competitor analysis
        for call in self.mock_repository.search_ads.call_args_list:
            query = call[0][0]
            assert query.ad_active_status == AdActiveStatus.ACTIVE
    
    @pytest.mark.asyncio
    async def test_get_competitor_ads_empty_keywords(self):
        """Test competitor analysis with empty keywords raises error"""
        with pytest.raises(InvalidSearchQueryError, match="At least one keyword is required"):
            await self.service.get_competitor_ads([])
    
    @pytest.mark.asyncio
    async def test_get_competitor_ads_skips_empty_keywords(self):
        """Test competitor analysis skips empty keywords"""
        keywords = ["fitness app", "", "workout tracker", "  "]
        
        self.mock_repository.search_ads = AsyncMock(
            return_value=AdSearchResult(ads=[], total_count=0)
        )
        
        results = await self.service.get_competitor_ads(keywords)
        
        # Should only call for non-empty keywords
        assert self.mock_repository.search_ads.call_count == 2
    
    @pytest.mark.asyncio
    async def test_search_by_page_name(self):
        """Test search by page name"""
        expected_result = AdSearchResult(ads=[], total_count=0)
        self.mock_repository.search_ads = AsyncMock(return_value=expected_result)
        
        result = await self.service.search_by_page_name("Test Page")
        
        assert result == expected_result
        
        # Verify query used page name as search terms
        call_args = self.mock_repository.search_ads.call_args
        query = call_args[0][0]
        assert query.search_terms == "Test Page"
        assert query.ad_active_status == AdActiveStatus.ALL
    
    def test_filter_ads_by_platform(self):
        """Test filtering ads by platform"""
        # Create ads with different platforms
        ads = [
            FacebookAd(id="1", publisher_platforms=[PublisherPlatform.FACEBOOK]),
            FacebookAd(id="2", publisher_platforms=[PublisherPlatform.INSTAGRAM]),
            FacebookAd(id="3", publisher_platforms=[PublisherPlatform.FACEBOOK, PublisherPlatform.INSTAGRAM]),
            FacebookAd(id="4", publisher_platforms=[PublisherPlatform.MESSENGER])
        ]
        
        # Filter by Facebook only
        facebook_ads = self.service.filter_ads_by_platform(ads, ["facebook"])
        assert len(facebook_ads) == 2  # ads 1 and 3
        assert facebook_ads[0].id == "1"
        assert facebook_ads[1].id == "3"
        
        # Filter by Instagram only
        instagram_ads = self.service.filter_ads_by_platform(ads, ["instagram"])
        assert len(instagram_ads) == 2  # ads 2 and 3
        
        # Filter by both Facebook and Instagram
        both_platforms = self.service.filter_ads_by_platform(ads, ["facebook", "instagram"])
        assert len(both_platforms) == 3  # ads 1, 2, and 3
    
    def test_get_ads_summary_empty_result(self):
        """Test summary generation for empty results"""
        result = AdSearchResult(ads=[], total_count=0)
        summary = self.service.get_ads_summary(result)
        
        expected = {
            'total_ads': 0,
            'active_ads': 0,
            'platforms': {},
            'pages': {},
            'has_more_pages': False
        }
        assert summary == expected
    
    def test_get_ads_summary_with_ads(self):
        """Test summary generation with ads"""
        ads = [
            FacebookAd(
                id="1", 
                page_name="Page A", 
                publisher_platforms=[PublisherPlatform.FACEBOOK],
                ad_delivery_stop_time=None  # Active
            ),
            FacebookAd(
                id="2", 
                page_name="Page B", 
                publisher_platforms=[PublisherPlatform.INSTAGRAM],
                ad_delivery_stop_time=None  # Active
            ),
            FacebookAd(
                id="3", 
                page_name="Page A", 
                publisher_platforms=[PublisherPlatform.FACEBOOK, PublisherPlatform.INSTAGRAM],
                ad_delivery_stop_time=None  # Active
            )
        ]
        
        result = AdSearchResult(
            ads=ads, 
            total_count=3, 
            next_page_url="https://example.com/next"
        )
        summary = self.service.get_ads_summary(result)
        
        assert summary['total_ads'] == 3
        assert summary['active_ads'] == 3  # All are active
        assert summary['platforms']['facebook'] == 2  # ads 1 and 3
        assert summary['platforms']['instagram'] == 2  # ads 2 and 3
        assert summary['top_pages']['Page A'] == 2  # ads 1 and 3
        assert summary['top_pages']['Page B'] == 1  # ad 2
        assert summary['has_more_pages'] is True
    
    @pytest.mark.asyncio
    async def test_close_calls_repository_close(self):
        """Test that close method calls repository close"""
        self.mock_repository.close = AsyncMock()
        
        await self.service.close()
        
        self.mock_repository.close.assert_called_once()
    
    @pytest.mark.asyncio 
    async def test_repository_error_propagation(self):
        """Test that repository errors are properly propagated"""
        self.mock_repository.search_ads = AsyncMock(
            side_effect=FacebookApiError("API Error")
        )
        
        with pytest.raises(FacebookApiError, match="API Error"):
            await self.service.search_ads("fitness")