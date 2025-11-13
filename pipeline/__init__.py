"""
Pipeline package for Klovis.

Provides a high-level orchestration class (KlovisPipeline) that allows chaining
of different preprocessing modules such as loaders, cleaners, chunkers, and metadata generators.
"""

from .pipeline import KlovisPipeline

__all__ = ["KlovisPipeline"]
