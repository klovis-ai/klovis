from abc import ABC, abstractmethod
from typing import List, Dict


class BaseMetadataGenerator(ABC):
    """
    Abstract base class for metadata generation.
    Used for creating embeddings, Q/A pairs, tags, and semantic information.
    """

    @abstractmethod
    def generate(self, chunks: List[Dict]) -> List[Dict]:
        """
        Generate metadata for each data chunk.
        Returns
        -------
        List[Dict]
            Chunks enriched with metadata.
        """
        pass
