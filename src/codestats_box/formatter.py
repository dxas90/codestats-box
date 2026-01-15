"""Gist content formatter."""

from .config import Settings, StatsType
from .models import FormattedLine, LanguageStats, UserStats
from .utils import format_xp_only, format_xp_value


class GistFormatter:
    """Formats Code::Stats data for GitHub Gist display."""

    GIST_TITLES = {
        StatsType.LEVEL_XP: "🧑🏻‍💻 My Code::Stats XP (Top Languages)",
        StatsType.RECENT_XP: "🧑🏻‍💻 My Code::Stats XP (Recent Languages)",
        StatsType.XP: "🧑🏻‍💻 My Code::Stats XP (Top Languages)",
    }

    NO_RECENT_ACTIVITY = [
        FormattedLine("Not been coding recently", "🙈"),
        FormattedLine("Probably busy with something else", "🗓"),
        FormattedLine("Or just taking a break", "🌴"),
        FormattedLine("But would be back to it soon!", "🤓"),
    ]

    def __init__(self, settings: Settings) -> None:
        """Initialize formatter.

        Args:
            settings: Application settings
        """
        self.settings = settings

    def get_title(self) -> str:
        """Get gist title based on stats type.

        Returns:
            Formatted gist title
        """
        return self.GIST_TITLES[self.settings.stats_type]

    def format_content(self, stats: UserStats) -> str:
        """Format user stats into gist content.

        Args:
            stats: User statistics to format

        Returns:
            Formatted content string ready for gist
        """
        lines = self._get_formatted_lines(stats)
        separator = ":"
        width = self.settings.max_line_length

        return "\n".join(line.format(separator, width) for line in lines)

    def _get_formatted_lines(self, stats: UserStats) -> list[FormattedLine]:
        """Get all formatted lines for the gist.

        Args:
            stats: User statistics

        Returns:
            List of formatted lines
        """
        lines = [self._format_total_line(stats)]

        language_lines = self._format_language_lines(stats.languages)
        lines.extend(language_lines)

        return lines

    def _format_total_line(self, stats: UserStats) -> FormattedLine:
        """Format the total XP line.

        Args:
            stats: User statistics

        Returns:
            Formatted line for total XP
        """
        if self.settings.stats_type == StatsType.XP:
            value = format_xp_only(stats.total_xp)
        elif self.settings.stats_type == StatsType.RECENT_XP:
            value = format_xp_value(stats.total_xp, stats.level, stats.new_xp)
        else:  # LEVEL_XP
            value = format_xp_value(stats.total_xp, stats.level)

        return FormattedLine("Total XP", value)

    def _format_language_lines(
        self, languages: list[LanguageStats]
    ) -> list[FormattedLine]:
        """Format lines for each language.

        Args:
            languages: List of language statistics

        Returns:
            List of formatted lines for languages
        """
        stats_type = self.settings.stats_type
        top_count = self.settings.top_languages_count

        # Filter and sort based on stats type
        if stats_type == StatsType.RECENT_XP:
            # Show languages with recent activity, sorted by recent XP
            active_languages = [lang for lang in languages if lang.new_xp > 0]
            sorted_languages = sorted(
                active_languages, key=lambda x: x.new_xp, reverse=True
            )[:top_count]

            # If no recent activity, show friendly message
            if not sorted_languages:
                return self.NO_RECENT_ACTIVITY
        else:
            # Show top languages by total XP
            sorted_languages = sorted(
                languages, key=lambda x: x.xp, reverse=True
            )[:top_count]

        # Format each language line
        return [
            self._format_language_line(lang) for lang in sorted_languages
        ]

    def _format_language_line(self, lang: LanguageStats) -> FormattedLine:
        """Format a single language line.

        Args:
            lang: Language statistics

        Returns:
            Formatted line for the language
        """
        if self.settings.stats_type == StatsType.XP:
            value = format_xp_only(lang.xp)
        elif self.settings.stats_type == StatsType.RECENT_XP:
            value = format_xp_value(lang.xp, lang.level, lang.new_xp)
        else:  # LEVEL_XP
            value = format_xp_value(lang.xp, lang.level)

        return FormattedLine(lang.name, value)
