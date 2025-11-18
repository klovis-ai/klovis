from abc import ABC, abstractmethod
from typing import List


class BaseEmbedder(ABC):
    """
    Abstract base class for text embedding models.
    """

    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate vector embeddings for a list of input texts.

        Parameters
        ----------
        texts : List[str]
            A list of text strings to embed.

        Returns
        -------
        List[List[float]]
            List of embedding vectors (one per input text).
        """
        pass
