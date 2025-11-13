from abc import ABC, abstractmethod
from typing import List, Dict


class BaseChunker(ABC):
    """
    Abstract base class for chunking strategies.
    Defines how data is split into smaller, meaningful units for RAG systems.
    """

    @abstractmethod
    def chunk(self, data: List[Dict]) -> List[Dict]:
        """
        Split cleaned data into smaller chunks.
        Returns
        -------
        List[Dict]
            Chunked data, ready for metadata generation or embedding.
        """
        pass
