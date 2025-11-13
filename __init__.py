"""
Klovis - Data preprocessing toolkit for RAG and LLM pipelines.
"""

from importlib.metadata import version

# Core components
from klovis.pipeline.pipeline import KlovisPipeline

# Loaders
from klovis.loaders import (
    TextFileLoader,
    PDFLoader,
    JSONLoader,
    HTMLLoader,
    DirectoryLoader,
    MultiLoader,
)

# Cleaners
from klovis.cleaning import (
    HTMLCleaner,
    TextCleaner,
    NormalizeCleaner,
    EmojiCleaner,
    CompositeCleaner,
)

# Base classes and models
from klovis.models import Document
from klovis.base import BaseLoader, BaseCleaner
from klovis.utils import get_logger

__all__ = [
    # Models
    "Document",

    # Base classes
    "BaseLoader",
    "BaseCleaner",

    # Loaders
    "TextFileLoader",
    "PDFLoader",
    "JSONLoader",
    "HTMLLoader",
    "DirectoryLoader",
    "MultiLoader",

    # Cleaners
    "HTMLCleaner",
    "TextCleaner",
    "NormalizeCleaner",
    "EmojiCleaner",
    "CompositeCleaner",

    # Pipeline
    "KlovisPipeline",

    # Utils
    "get_logger",
]


def __getattr__(name: str):
    """
    Allows dynamic access to package metadata.
    Example: klovis.__version__
    """
    if name == "__version__":
        try:
            return version("klovis")
        except Exception:
            return "0.1.0"
    raise AttributeError(f"module 'klovis' has no attribute '{name}'")
