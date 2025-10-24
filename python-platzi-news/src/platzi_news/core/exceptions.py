"""Custom exceptions for Platzi News."""


class PlatziNewsError(Exception):
    """Base exception for Platzi News application."""

    pass


class ConfigError(PlatziNewsError):
    """Raised when there are configuration issues."""

    pass


class APIError(PlatziNewsError):
    """Raised when there are API-related errors."""

    pass


class AnalysisError(PlatziNewsError):
    """Raised when there are analysis-related errors."""

    pass


class SourceError(PlatziNewsError):
    """Raised when there are news source-related errors."""

    pass
