import os
import asyncio
from typing import List, Dict, Any, Optional
from apify_client import ApifyClient
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class ApifyService:
    """Service for interacting with Apify Facebook Ads Library scraper."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Apify service.

        Args:
            api_key: Apify API key. If not provided, reads from APIFY_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get('APIFY_API_KEY')
        if not self.api_key:
            raise ValueError("APIFY_API_KEY must be provided or set as environment variable")

        self.client = ApifyClient(self.api_key)
        self.actor_name = os.environ.get('APIFY_ACTOR_NAME', 'curious_coder/facebook-ads-library-scraper')

    def _run_apify_sync(self, url: str, max_results: int, fetch_all_details: bool) -> List[Dict[str, Any]]:
        """
        Synchronous method to run Apify actor.
        This will be executed in a thread pool to avoid blocking the event loop.
        """
        # Ensure URL has media_type=video for filtering at Facebook level
        processed_url = self._ensure_video_filter_in_url(url)
        
        # Ensure minimum count of 10 (actor requirement)
        actor_count = max(10, max_results * 3)  # Request more to account for filtering
        
        run_input = {
            "urls": [{"url": processed_url}],
            "count": actor_count,
            "period": "",
            "scrapePageAds.activeStatus": "all",
            "scrapePageAds.countryCode": "ALL",
        }

        logger.info(f"Starting Apify actor for URL: {url} (requested: {max_results}, actor_count: {actor_count})")
        logger.info(f"Actor input: {run_input}")

        # Run the actor and wait for it to finish
        run = self.client.actor(self.actor_name).call(run_input=run_input)

        logger.info(f"Actor completed. Dataset ID: {run['defaultDatasetId']}")

        # Fetch the results from the dataset
        raw_results = []
        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            raw_results.append(item)

        logger.info(f"Raw results from actor: {len(raw_results)} items")

        # Filter by video ads only (client-side filtering as backup)
        video_results = self._filter_video_ads(raw_results)
        
        # Apply max_results limit (client-side enforcement)
        limited_results = video_results[:max_results]
        
        logger.info(f"After filtering: {len(video_results)} video ads, taking {len(limited_results)} max")
        return limited_results

    def _filter_video_ads(self, ads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter ads to include only those with video content.
        """
        video_ads = []
        
        for ad in ads:
            has_video = False
            
            # Check for videos in snapshot
            snapshot = ad.get('snapshot', {})
            
            # Check videos array
            videos = snapshot.get('videos', [])
            if videos and len(videos) > 0:
                has_video = True
            
            # Check cards for video content
            cards = snapshot.get('cards', [])
            for card in cards:
                if card.get('video_hd_url') or card.get('video_sd_url'):
                    has_video = True
                    break
            
            if has_video:
                video_ads.append(ad)
            else:
                logger.debug(f"Skipping non-video ad: {ad.get('ad_archive_id', 'unknown')}")
        
        return video_ads

    def _ensure_video_filter_in_url(self, url: str) -> str:
        """
        Ensure the Facebook Ads Library URL has media_type=video parameter.
        """
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
        
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        
        # Set media_type to video
        query_params['media_type'] = ['video']
        
        # If search is too broad, we might not get results - log this
        if 'q' not in query_params and 'view_all_page_id' not in query_params:
            logger.warning("URL has no specific search term or page_id - might return too many results")
        
        # Reconstruct URL
        new_query = urlencode(query_params, doseq=True)
        new_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))
        
        if new_url != url:
            logger.info(f"Modified URL to include video filter: {new_url}")
        
        return new_url

    async def extract_ads_from_url(
        self,
        url: str,
        max_results: int = 15,
        fetch_all_details: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Extract ads from Facebook Ads Library URL using Apify.
        
        Runs blocking Apify calls in a thread pool to avoid blocking the event loop.

        Args:
            url: Facebook Ads Library URL
            max_results: Maximum number of ads to extract
            fetch_all_details: Whether to fetch full creative details

        Returns:
            List of ad data dictionaries

        Raises:
            Exception: If the Apify actor run fails
        """
        try:
            # Run blocking Apify code in thread pool
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                results = await loop.run_in_executor(
                    executor,
                    self._run_apify_sync,
                    url,
                    max_results,
                    fetch_all_details
                )
            return results

        except Exception as e:
            logger.error(f"Error running Apify actor: {str(e)}")
            raise Exception(f"Failed to extract ads: {str(e)}")
