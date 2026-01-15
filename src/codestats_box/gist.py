"""GitHub Gist updater."""

import structlog
from github import Github
from github.GistFile import GistFile
from github.InputFileContent import InputFileContent

from .config import Settings
from .exceptions import GitHubAPIError

logger = structlog.get_logger(__name__)


class GistUpdater:
    """Manages GitHub Gist updates."""

    def __init__(self, settings: Settings) -> None:
        """Initialize gist updater.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.github = Github(settings.gh_token)

    def update_gist(self, title: str, content: str) -> bool:
        """Update the configured gist with new content.

        Args:
            title: Gist filename
            content: Content to write to gist

        Returns:
            True if gist was updated, False if no changes needed

        Raises:
            GitHubAPIError: If gist update fails
        """
        gist_id = self.settings.gist_id

        logger.info(
            "updating_gist",
            gist_id=gist_id,
            title=title,
            content_length=len(content),
        )

        try:
            gist = self.github.get_gist(gist_id)
        except Exception as e:
            logger.error(
                "gist_fetch_error",
                gist_id=gist_id,
                error=str(e),
            )
            raise GitHubAPIError(f"Failed to fetch gist {gist_id}: {e}") from e

        # Get current content (first file in gist)
        if not gist.files:
            logger.error("gist_empty", gist_id=gist_id)
            raise GitHubAPIError(f"Gist {gist_id} has no files")

        old_title = list(gist.files.keys())[0]
        old_file: GistFile = gist.files[old_title]
        current_content = old_file.content

        # Check if update is needed
        if current_content == content and old_title == title:
            logger.info(
                "gist_unchanged",
                gist_id=gist_id,
                title=title,
            )
            return False

        # Update gist
        try:
            gist.edit(
                files={old_title: InputFileContent(content, title)}
            )
            logger.info(
                "gist_updated",
                gist_id=gist_id,
                old_title=old_title,
                new_title=title,
                content_length=len(content),
            )
            return True

        except Exception as e:
            logger.error(
                "gist_update_error",
                gist_id=gist_id,
                error=str(e),
            )
            raise GitHubAPIError(f"Failed to update gist {gist_id}: {e}") from e

    def close(self) -> None:
        """Close GitHub client connection."""
        # PyGithub doesn't require explicit cleanup, but included for consistency
        pass
