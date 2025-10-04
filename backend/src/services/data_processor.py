from datetime import datetime
from typing import List, Dict, Any
from src.api.models import AdCreative, AdCard
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Process raw Apify response data into structured models."""

    @staticmethod
    def process_ads(raw_data: List[Dict[str, Any]]) -> List[AdCreative]:
        """
        Process raw Apify data into structured AdCreative models.

        Args:
            raw_data: List of raw ad data from Apify

        Returns:
            List of AdCreative objects
        """
        processed_ads = []

        for item in raw_data:
            try:
                ad = DataProcessor._process_single_ad(item)
                processed_ads.append(ad)
            except Exception as e:
                logger.warning(f"Failed to process ad {item.get('ad_archive_id', 'unknown')}: {str(e)}")
                continue

        return processed_ads

    @staticmethod
    def _process_single_ad(item: Dict[str, Any]) -> AdCreative:
        """Process a single ad item."""
        snapshot = item.get('snapshot', {})

        # Process cards
        cards_data = snapshot.get('cards', [])
        cards = [DataProcessor._process_card(card) for card in cards_data]

        # Extract image and video URLs from cards and snapshot.videos
        image_urls = []
        video_urls = []

        # From cards
        for card in cards_data:
            if card.get('original_image_url'):
                image_urls.append(card['original_image_url'])
            if card.get('resized_image_url'):
                image_urls.append(card['resized_image_url'])
            if card.get('video_hd_url'):
                video_urls.append(card['video_hd_url'])
            elif card.get('video_sd_url'):
                video_urls.append(card['video_sd_url'])

        # From snapshot.videos
        for v in snapshot.get('videos', []) or []:
            if v.get('video_hd_url'):
                video_urls.append(v['video_hd_url'])
            elif v.get('video_sd_url'):
                video_urls.append(v['video_sd_url'])

        # Remove duplicates while preserving order
        image_urls = list(dict.fromkeys(image_urls))
        video_urls = list(dict.fromkeys(video_urls))

        # Process body text
        body_data = snapshot.get('body', {})
        body_text = body_data.get('text') if isinstance(body_data, dict) else None

        # Convert timestamps to datetime
        start_date = None
        end_date = None
        if item.get('start_date'):
            start_date = datetime.fromtimestamp(item['start_date'])
        if item.get('end_date'):
            end_date = datetime.fromtimestamp(item['end_date'])

        return AdCreative(
            ad_archive_id=item.get('ad_archive_id', ''),
            ad_id=item.get('ad_id'),
            page_id=item.get('page_id', ''),
            page_name=snapshot.get('page_name', ''),
            page_profile_uri=snapshot.get('page_profile_uri'),
            page_profile_picture_url=snapshot.get('page_profile_picture_url'),
            page_categories=snapshot.get('page_categories', []),
            page_like_count=snapshot.get('page_like_count'),
            body=body_text,
            title=snapshot.get('title'),
            caption=snapshot.get('caption'),
            link_url=snapshot.get('link_url'),
            link_description=snapshot.get('link_description'),
            cta_text=snapshot.get('cta_text'),
            cta_type=snapshot.get('cta_type'),
            display_format=snapshot.get('display_format'),
            cards=cards,
            image_urls=image_urls,
            video_urls=video_urls,
            start_date=start_date,
            end_date=end_date,
            start_date_formatted=item.get('start_date_formatted'),
            end_date_formatted=item.get('end_date_formatted'),
            publisher_platform=item.get('publisher_platform', []),
            is_active=item.get('is_active', False),
            categories=item.get('categories', []),
            ad_library_url=item.get('ad_library_url', ''),
            url=item.get('url'),
            total=item.get('total'),
            ads_count=item.get('ads_count'),
            collation_count=item.get('collation_count'),
        )

    @staticmethod
    def _process_card(card_data: Dict[str, Any]) -> AdCard:
        """Process a single card."""
        return AdCard(
            body=card_data.get('body'),
            title=card_data.get('title'),
            caption=card_data.get('caption'),
            link_url=card_data.get('link_url'),
            link_description=card_data.get('link_description'),
            cta_text=card_data.get('cta_text'),
            cta_type=card_data.get('cta_type'),
            original_image_url=card_data.get('original_image_url'),
            resized_image_url=card_data.get('resized_image_url'),
            video_hd_url=card_data.get('video_hd_url'),
            video_sd_url=card_data.get('video_sd_url'),
            video_preview_image_url=card_data.get('video_preview_image_url'),
        )
