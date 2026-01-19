import time
import logging
from typing import Callable, TypeVar, Any

logger = logging.getLogger(__name__)

T = TypeVar("T")


RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}
RETRYABLE_ERROR_TYPES = (
    "APIConnectionError",
    "APITimeoutError",
    "RateLimitError",
    "InternalServerError",
    "ServiceUnavailableError",
)


def is_retryable(error: Exception) -> bool:
    error_type = type(error).__name__
    if error_type in RETRYABLE_ERROR_TYPES:
        return True
    
    if hasattr(error, "status_code"):
        return error.status_code in RETRYABLE_STATUS_CODES
    
    error_msg = str(error).lower()
    return any(term in error_msg for term in ["timeout", "connection", "rate limit", "overloaded"])


def retry_with_backoff(
    func: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    should_retry: Callable[[Exception], bool] = is_retryable,
) -> T:
    last_error = None
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_error = e
            
            if not should_retry(e) or attempt == max_retries - 1:
                raise
            
            delay = min(base_delay * (2 ** attempt), max_delay)
            logger.warning(
                f"Request failed (attempt {attempt + 1}/{max_retries}): {e}. "
                f"Retrying in {delay:.1f}s..."
            )
            time.sleep(delay)
    
    raise last_error
