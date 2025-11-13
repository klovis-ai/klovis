from abc import ABC, abstractmethod
from typing import Any, List, Dict


class BaseLoader(ABC):
    """
    Abstract base class for all document loaders.
    Defines the interface for loading and parsing one or multiple documents.
    """

    @abstractmethod
    def load(self, sources: List[Any]) -> List[Dict]:
        """
        Load data from one or more sources (files, URLs, databases, etc.).
        Returns
        -------
        List[Dict]
            A list of dictionaries representing loaded documents.
        """
        pass
