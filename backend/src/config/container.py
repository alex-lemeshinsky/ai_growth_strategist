"""
Dependency Injection container for the application.
Manages the creation and lifecycle of dependencies.
"""

from typing import Optional, Dict, Any
from domain.interfaces import IFacebookAdsRepository, IConfigurationService
from infrastructure.facebook_ads_repository import FacebookAdsRepository
from infrastructure.configuration_service import ConfigurationService
from application.ads_search_service import AdsSearchService


class DIContainer:
    """
    Simple dependency injection container.
    Manages creation and caching of service instances.
    """
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._initialized = False
    
    def initialize(self, env_file: Optional[str] = None):
        """
        Initialize the container with all dependencies.
        
        Args:
            env_file: Optional path to .env file for configuration
        """
        if self._initialized:
            return
        
        # Configuration service (singleton)
        config_service = ConfigurationService(env_file)
        self._services['config'] = config_service
        
        # Facebook Ads Repository (singleton)
        ads_repository = FacebookAdsRepository(config_service)
        self._services['ads_repository'] = ads_repository
        
        # Ads Search Service (singleton)
        ads_search_service = AdsSearchService(ads_repository, config_service)
        self._services['ads_search_service'] = ads_search_service
        
        self._initialized = True
    
    def get_config_service(self) -> IConfigurationService:
        """Get configuration service instance"""
        return self._services['config']
    
    def get_ads_repository(self) -> IFacebookAdsRepository:
        """Get Facebook Ads repository instance"""
        return self._services['ads_repository']
    
    def get_ads_search_service(self) -> AdsSearchService:
        """Get Ads Search service instance"""
        return self._services['ads_search_service']
    
    async def close(self):
        """Close all services that need cleanup"""
        # Close ads repository if it has a close method
        ads_repository = self._services.get('ads_repository')
        if ads_repository and hasattr(ads_repository, 'close'):
            await ads_repository.close()
        
        # Close ads search service
        ads_search_service = self._services.get('ads_search_service')
        if ads_search_service and hasattr(ads_search_service, 'close'):
            await ads_search_service.close()


# Global container instance
container = DIContainer()