"""
Base module for Klovis.

Contains abstract classes defining the core architecture for data preprocessing:
loaders, extractors, cleaners, chunkers, and metadata generators.
"""

from .base_loader import BaseLoader
from .base_extractor import BaseExtractor
from .base_cleaner import BaseCleaner
from .base_chunker import BaseChunker
from .base_metadata import BaseMetadataGenerator

__all__ = [
    "BaseLoader",
    "BaseExtractor",
    "BaseCleaner",
    "BaseChunker",
    "BaseMetadataGenerator",
]
