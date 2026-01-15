"""Code::Stats API client with retry logic."""

from typing import Any

import httpx
import structlog
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .config import Settings
from .exceptions import CodeStatsAPIError
from .models import UserStats

logger = structlog.get_logger(__name__)


class CodeStatsClient:
    """Client for interacting with Code::Stats API."""

    def __init__(self, settings: Settings) -> None:
        """Initialize Code::Stats client.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.client = httpx.Client(
            timeout=30.0,
            follow_redirects=True,
        )

    def __enter__(self) -> "CodeStatsClient":
        """Context manager entry."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit - close HTTP client."""
        self.client.close()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        reraise=True,
    )
    def get_user_stats(self) -> UserStats:
        """Fetch user statistics from Code::Stats API.

        Returns:
            UserStats object containing all user statistics

        Raises:
            CodeStatsAPIError: If the API request fails
        """
        url = self.settings.get_codestats_url()
        username = self.settings.code_stats_username

        logger.info(
            "fetching_codestats_data",
            username=username,
            url=url,
        )

        try:
            response = self.client.get(url)
            response.raise_for_status()
            data = response.json()

            logger.info(
                "codestats_data_fetched",
                username=username,
                total_xp=data.get("total_xp", 0),
                languages_count=len(data.get("languages", {})),
            )

            return UserStats.from_api_response(username, data)

        except httpx.HTTPStatusError as e:
            logger.error(
                "codestats_api_error",
                username=username,
                status_code=e.response.status_code,
                error=str(e),
            )
            raise CodeStatsAPIError(
                f"Failed to fetch Code::Stats data for user '{username}': "
                f"HTTP {e.response.status_code}"
            ) from e

        except httpx.RequestError as e:
            logger.error(
                "codestats_request_error",
                username=username,
                error=str(e),
            )
            raise CodeStatsAPIError(
                f"Network error while fetching Code::Stats data for user '{username}': {e}"
            ) from e

        except (KeyError, ValueError, TypeError) as e:
            logger.error(
                "codestats_data_parse_error",
                username=username,
                error=str(e),
            )
            raise CodeStatsAPIError(
                f"Failed to parse Code::Stats API response for user '{username}': {e}"
            ) from e
