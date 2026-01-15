"""Custom exceptions for Code::Stats Box."""


class CodeStatsBoxError(Exception):
    """Base exception for all Code::Stats Box errors."""


class ConfigurationError(CodeStatsBoxError):
    """Raised when configuration is invalid or missing."""


class APIError(CodeStatsBoxError):
    """Raised when an API call fails."""


class CodeStatsAPIError(APIError):
    """Raised when Code::Stats API call fails."""


class GitHubAPIError(APIError):
    """Raised when GitHub API call fails."""


class DataValidationError(CodeStatsBoxError):
    """Raised when data validation fails."""
