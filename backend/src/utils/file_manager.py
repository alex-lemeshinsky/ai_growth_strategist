import os
import json
from datetime import datetime
from typing import List, Optional
from pathlib import Path
import aiofiles
import logging

logger = logging.getLogger(__name__)


class FileManager:
    """Manage file operations for saving ad data."""

    def __init__(self, output_directory: str = "creatives"):
        """
        Initialize FileManager.

        Args:
            output_directory: Directory to save files (relative to backend/)
        """
        self.output_directory = output_directory
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """Create output directory if it doesn't exist."""
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)

    def generate_filename(
        self,
        page_name: Optional[str] = None,
        page_id: Optional[str] = None,
        custom_name: Optional[str] = None
    ) -> str:
        """
        Generate a filename for the output JSON file.

        Args:
            page_name: Page name from the ads
            page_id: Page ID from the ads
            custom_name: Custom filename (without extension)

        Returns:
            Generated filename with .json extension
        """
        if custom_name:
            filename = custom_name
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if page_name and page_id:
                # Clean page name for use in filename
                clean_page_name = page_name.replace(' ', '_').replace('/', '_')
                filename = f"{clean_page_name}_{page_id}_{timestamp}"
            else:
                filename = f"ads_{timestamp}"

        # Add .json extension if not present
        if not filename.endswith('.json'):
            filename += '.json'

        return filename

    async def save_ads(
        self,
        ads_data: List[dict],
        filename: Optional[str] = None,
        page_name: Optional[str] = None,
        page_id: Optional[str] = None
    ) -> str:
        """
        Save ads data to JSON file.

        Args:
            ads_data: List of ad data to save
            filename: Custom filename (optional)
            page_name: Page name for auto-generated filename
            page_id: Page ID for auto-generated filename

        Returns:
            Path to the saved file
        """
        filename = self.generate_filename(page_name, page_id, filename)
        filepath = os.path.join(self.output_directory, filename)

        try:
            # Convert to JSON-serializable format
            json_data = [ad.dict() if hasattr(ad, 'dict') else ad for ad in ads_data]

            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(json_data, indent=2, ensure_ascii=False, default=str))

            logger.info(f"Saved {len(ads_data)} ads to {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Error saving file {filepath}: {str(e)}")
            raise Exception(f"Failed to save file: {str(e)}")

    def file_exists(self, filename: str) -> bool:
        """Check if a file exists in the output directory."""
        filepath = os.path.join(self.output_directory, filename)
        return os.path.exists(filepath)

    def get_file_path(self, filename: str) -> str:
        """Get full path for a filename."""
        return os.path.join(self.output_directory, filename)
