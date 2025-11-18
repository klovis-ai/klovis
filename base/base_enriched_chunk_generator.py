from abc import ABC, abstractmethod
from typing import List
from klovis.models import Chunk

class BaseEnrichedChunkGenerator(ABC):
    """
    Base class for generators that produce NEW chunks
    derived from source chunks.
    """

    @abstractmethod
    def generate(self, chunk: Chunk) -> List[Chunk]:
        """
        Returns a list of new Chunk objects.
        """
        pass
