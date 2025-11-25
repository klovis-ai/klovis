from abc import ABC, abstractmethod
from typing import Any, List, Dict, Iterator


class BaseLoader(ABC):
    """
    Abstract base class for all document loaders.
    Defines the interface for loading and parsing one or multiple documents.
    """

    @abstractmethod
    def load(self, sources: List[Any] = None) -> List[Dict]:
        """
        Load data from one or more sources (files, URLs, databases, etc.).
        Returns
        -------
        List[Dict]
            A list of dictionaries representing loaded documents.
        """
        pass

    def load_stream(self, sources: List[Any] = None) -> Iterator[Dict]:
        """
        Lazy load data from sources.
        Default implementation wraps load() but subclasses should override for true streaming.
        
        Returns
        -------
        Iterator[Dict]
            An iterator of dictionaries representing loaded documents.
        """
        return iter(self.load(sources))
