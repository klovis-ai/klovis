from typing import List, Dict
from klovis.base import BaseExtractor
from klovis.config import settings
from klovis.exceptions import MissingAPIKeyError


class VLExtractor(BaseExtractor):
    """
    Example of a Vision-Language extractor.

    This class demonstrates how to enforce API key presence
    before running a model-dependent feature.
    """

    def __init__(self):
        if not settings.has_api_key():
            raise MissingAPIKeyError("Klovis API key required for Vision-Language extraction.")

    def extract(self, data: List[Dict]) -> List[Dict]:
        for doc in data:
            doc["extracted_text"] = f"Extracted features from: {doc.get('source')}"
        return data
