"""Data models for Code::Stats API responses."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LanguageStats:
    """Statistics for a single programming language."""

    name: str
    xp: int
    new_xp: int = 0
    level: int = 0

    @classmethod
    def from_api_response(cls, name: str, data: dict[str, Any]) -> "LanguageStats":
        """Create LanguageStats from Code::Stats API response."""
        from .utils import calculate_level

        xp = data.get("xps", 0)
        new_xp = data.get("new_xps", 0)
        level = calculate_level(xp)

        return cls(
            name=name,
            xp=xp,
            new_xp=new_xp,
            level=level,
        )


@dataclass(frozen=True)
class UserStats:
    """Complete statistics for a Code::Stats user."""

    username: str
    total_xp: int
    new_xp: int
    level: int
    languages: list[LanguageStats]

    @classmethod
    def from_api_response(cls, username: str, data: dict[str, Any]) -> "UserStats":
        """Create UserStats from Code::Stats API response."""
        from .utils import calculate_level

        total_xp = data.get("total_xp", 0)
        new_xp = data.get("new_xp", 0)
        level = calculate_level(total_xp)

        languages_data = data.get("languages", {})
        languages = [
            LanguageStats.from_api_response(name, lang_data)
            for name, lang_data in languages_data.items()
        ]

        return cls(
            username=username,
            total_xp=total_xp,
            new_xp=new_xp,
            level=level,
            languages=languages,
        )


@dataclass(frozen=True)
class FormattedLine:
    """A single formatted line for the gist content."""

    title: str
    value: str

    def format(self, separator: str, width: int) -> str:
        """Format the line with proper spacing."""
        available_space = width - len(self.title) - len(self.value) - 2
        sep = f" {separator * max(available_space, 1)} "
        return f"{self.title}{sep}{self.value}"
