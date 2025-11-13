from abc import ABC, abstractmethod
from typing import List, Dict


class BaseExtractor(ABC):
    """
    Abstract base class for all extractors.
    Used for extracting structured, semantic, or visual information from raw data.
    """

    @abstractmethod
    def extract(self, data: List[Dict]) -> List[Dict]:
        """
        Perform information extraction on the loaded data.
        Returns
        -------
        List[Dict]
            A list of dictionaries with enriched or transformed data.
        """
        pass
