from abc import ABC, abstractmethod
from klovis.models import Chunk

class BaseMetadataGenerator(ABC):

    @abstractmethod
    def generate(self, chunk: Chunk) -> dict:
        """
        Generate metadata for a single chunk.
        Returns a dict that will be merged into chunk.metadata.
        """
        pass
