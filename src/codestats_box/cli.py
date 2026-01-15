"""Command-line interface for Code::Stats Box."""

import sys
from pathlib import Path

import structlog
from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .api import CodeStatsClient
from .config import Settings
from .exceptions import CodeStatsBoxError
from .formatter import GistFormatter
from .gist import GistUpdater
from .logging_config import configure_logging

logger = structlog.get_logger(__name__)
console = Console()


def print_error(message: str) -> None:
    """Print error message in red.

    Args:
        message: Error message to display
    """
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print success message in green.

    Args:
        message: Success message to display
    """
    console.print(f"[bold green]✓[/bold green] {message}")


def print_info(message: str) -> None:
    """Print info message.

    Args:
        message: Info message to display
    """
    console.print(f"[bold blue]ℹ[/bold blue] {message}")


def display_content(title: str, content: str) -> None:
    """Display formatted content in a panel.

    Args:
        title: Panel title
        content: Content to display
    """
    text = Text(content, style="cyan")
    panel = Panel(text, title=title, border_style="blue")
    console.print(panel)


def run() -> int:
    """Main execution function.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Load configuration
        settings = Settings()
        configure_logging(settings.log_level)

        logger.info(
            "starting_codestats_box",
            username=settings.code_stats_username,
            stats_type=settings.stats_type.value,
        )

        # Fetch Code::Stats data
        with CodeStatsClient(settings) as client:
            stats = client.get_user_stats()

        # Format content
        formatter = GistFormatter(settings)
        title = formatter.get_title()
        content = formatter.format_content(stats)

        # Display content preview
        display_content(title, content)

        # Update gist
        updater = GistUpdater(settings)
        was_updated = updater.update_gist(title, content)

        if was_updated:
            print_success("Gist updated successfully!")
        else:
            print_info("Gist is already up to date. No changes needed.")

        logger.info(
            "codestats_box_completed",
            updated=was_updated,
            total_xp=stats.total_xp,
            languages_count=len(stats.languages),
        )

        return 0

    except ValidationError as e:
        print_error("Configuration validation failed:")
        console.print(e)
        logger.error("config_validation_error", error=str(e))
        return 1

    except CodeStatsBoxError as e:
        print_error(str(e))
        logger.error("application_error", error=str(e), error_type=type(e).__name__)
        return 1

    except KeyboardInterrupt:
        print_info("Operation cancelled by user")
        logger.info("operation_cancelled")
        return 130

    except Exception as e:
        print_error(f"Unexpected error: {e}")
        logger.exception("unexpected_error", error=str(e))
        return 1


def test_mode() -> int:
    """Test mode for local development.

    Returns:
        Exit code
    """
    args = sys.argv[2:]  # Skip 'test' command

    if len(args) < 2:
        print_error("Usage: codestats-box test <username> <stats-type> [gist-id] [token]")
        return 1

    # Override environment for testing
    import os
    os.environ["CODE_STATS_USERNAME"] = args[0]
    os.environ["STATS_TYPE"] = args[1]

    if len(args) >= 4:
        os.environ["GIST_ID"] = args[2]
        os.environ["GH_TOKEN"] = args[3]
    else:
        # Test mode without gist update
        os.environ["GIST_ID"] = "test-gist-id"
        os.environ["GH_TOKEN"] = "test-token"

    try:
        settings = Settings()
        configure_logging(settings.log_level)

        # Fetch and display stats
        with CodeStatsClient(settings) as client:
            stats = client.get_user_stats()

        formatter = GistFormatter(settings)
        title = formatter.get_title()
        content = formatter.format_content(stats)

        display_content(title, content)

        # Only update gist if credentials provided
        if len(args) >= 4:
            updater = GistUpdater(settings)
            updater.update_gist(title, content)
            print_success("Test completed with gist update!")
        else:
            print_info("Test completed (content only, no gist update)")

        return 0

    except Exception as e:
        print_error(f"Test failed: {e}")
        logger.exception("test_error", error=str(e))
        return 1


def main() -> None:
    """CLI entry point."""
    # Check for test mode
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sys.exit(test_mode())

    # Normal execution
    sys.exit(run())


if __name__ == "__main__":
    main()
