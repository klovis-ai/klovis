"""
Base Transformer class for Klovis data transformations.
"""

from abc import ABC, abstractmethod
from typing import List, Union
from klovis.models import Document


class BaseTransformer(ABC):
    """
    Abstract base class for data transformers.
    """

    @abstractmethod
    def transform(self, documents: List[Document]) -> Union[List[Document], List[dict]]:
        """
        Transforms a list of documents (or chunks) into a new structured representation.
        Must return a list (not a single string).
        """
        pass
