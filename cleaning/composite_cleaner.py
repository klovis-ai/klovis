"""
Composite cleaner for Klovis.
Combines multiple cleaning steps into a single, configurable pipeline.
"""

from typing import List, Type
from klovis.base import BaseCleaner
from klovis.models import Document
from klovis.utils import get_logger

logger = get_logger(__name__)


class CompositeCleaner(BaseCleaner):
    """
    Combines multiple cleaners into a sequential cleaning pipeline.

    Parameters
    ----------
    cleaners : List[BaseCleaner]
        List of cleaner instances to apply in order.
    """

    def __init__(self, cleaners: List[BaseCleaner]):
        if not cleaners or not all(isinstance(c, BaseCleaner) for c in cleaners):
            raise ValueError("CompositeCleaner requires a list of BaseCleaner instances.")
        self.cleaners = cleaners
        logger.debug(f"CompositeCleaner initialized with {len(cleaners)} cleaner(s).")

    def clean(self, documents: List[Document]) -> List[Document]:
        """
        Applies each cleaner sequentially to the documents.

        Parameters
        ----------
        documents : List[Document]
            List of documents to be cleaned.

        Returns
        -------
        List[Document]
            Cleaned and normalized documents.
        """
        current_docs = documents

        logger.info(f"CompositeCleaner: starting pipeline with {len(current_docs)} document(s).")

        for cleaner in self.cleaners:
            cleaner_name = cleaner.__class__.__name__
            logger.info(f"Running {cleaner_name}...")
            current_docs = cleaner.clean(current_docs)
            logger.info(f"{cleaner_name} completed → {len(current_docs)} document(s).")

        logger.info("CompositeCleaner pipeline completed successfully.")
        return current_docs
