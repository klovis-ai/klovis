from abc import ABC, abstractmethod
from typing import List, Dict


class BaseCleaner(ABC):
    """
    Abstract base class for data cleaning operations.
    Handles normalization, text cleaning, noise removal, etc.
    """

    @abstractmethod
    def clean(self, data: List[Dict]) -> List[Dict]:
        """
        Clean or normalize the provided data.
        Returns
        -------
        List[Dict]
            Cleaned and standardized data.
        """
        pass
