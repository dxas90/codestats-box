"""Configuration management using Pydantic Settings."""

from enum import Enum
from typing import Annotated

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class StatsType(str, Enum):
    """Type of statistics to display."""

    LEVEL_XP = "level-xp"
    RECENT_XP = "recent-xp"
    XP = "xp"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Required settings
    gh_token: Annotated[
        str,
        Field(
            description="GitHub personal access token with gist scope",
            min_length=1,
        ),
    ]

    gist_id: Annotated[
        str,
        Field(
            description="GitHub Gist ID to update",
            min_length=1,
        ),
    ]

    code_stats_username: Annotated[
        str,
        Field(
            description="Code::Stats username",
            min_length=1,
        ),
    ]

    # Optional settings with defaults
    stats_type: Annotated[
        StatsType,
        Field(
            default=StatsType.LEVEL_XP,
            description="Type of stats to display",
        ),
    ] = StatsType.LEVEL_XP

    top_languages_count: Annotated[
        int,
        Field(
            default=10,
            ge=1,
            le=50,
            description="Number of top languages to display",
        ),
    ] = 10

    codestats_api_base_url: Annotated[
        str,
        Field(
            default="https://codestats.net/api/users",
            description="Code::Stats API base URL",
        ),
    ] = "https://codestats.net/api/users"

    max_line_length: Annotated[
        int,
        Field(
            default=54,
            ge=40,
            le=100,
            description="Maximum line length for gist content",
        ),
    ] = 54

    # Retry configuration
    max_retries: Annotated[
        int,
        Field(
            default=3,
            ge=1,
            le=10,
            description="Maximum number of API call retries",
        ),
    ] = 3

    retry_backoff_factor: Annotated[
        float,
        Field(
            default=2.0,
            ge=1.0,
            le=10.0,
            description="Exponential backoff factor for retries",
        ),
    ] = 2.0

    # Logging
    log_level: Annotated[
        str,
        Field(
            default="INFO",
            description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
        ),
    ] = "INFO"

    def get_codestats_url(self) -> str:
        """Get the Code::Stats API URL for the configured username."""
        return f"{self.codestats_api_base_url}/{self.code_stats_username}"
