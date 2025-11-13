"""
Custom exception classes for the Klovis library.

This module defines the hierarchy of exceptions used throughout the library.
Each error type inherits from `KlovisError`, the base exception for all Klovis-specific errors.
"""


class KlovisError(Exception):
    """Base exception class for all Klovis errors."""
    pass


class MissingAPIKeyError(KlovisError):
    """Raised when the required Klovis API key is missing or invalid."""
    pass


class InvalidDataError(KlovisError):
    """Raised when input data is invalid, corrupted, or cannot be processed."""
    pass


class ProcessingError(KlovisError):
    """Raised when an internal processing step fails."""
    pass


class ModuleDependencyError(KlovisError):
    """Raised when a module depends on unavailable external libraries or models."""
    pass
