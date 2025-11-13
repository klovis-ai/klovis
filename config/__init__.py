"""
Configuration package for Klovis.

This package handles environment variables, API key validation,
and global settings management for the Klovis platform.
"""

from .settings import settings, Settings

__all__ = ["settings", "Settings"]