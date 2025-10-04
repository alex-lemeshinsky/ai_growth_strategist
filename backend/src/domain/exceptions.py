"""
Domain-specific exceptions.
These exceptions represent business logic errors and are independent of infrastructure.
"""


class FacebookDomainError(Exception):
    """Base exception for all Facebook domain errors"""
    pass


class FacebookApiError(FacebookDomainError):
    """Raised when Facebook API returns an error"""
    
    def __init__(self, message: str, error_code: str = None, http_status: int = None):
        super().__init__(message)
        self.error_code = error_code
        self.http_status = http_status


class AuthenticationError(FacebookDomainError):
    """Raised when authentication with Facebook fails"""
    pass


class AdNotFoundError(FacebookDomainError):
    """Raised when requested Facebook ad is not found"""
    
    def __init__(self, ad_id: str):
        super().__init__(f"Facebook ad with ID {ad_id} not found")
        self.ad_id = ad_id


class InvalidSearchQueryError(FacebookDomainError):
    """Raised when search query parameters are invalid"""
    pass


class RateLimitExceededError(FacebookDomainError):
    """Raised when Facebook API rate limit is exceeded"""
    
    def __init__(self, retry_after: int = None):
        message = "Facebook API rate limit exceeded"
        if retry_after:
            message += f", retry after {retry_after} seconds"
        super().__init__(message)
        self.retry_after = retry_after