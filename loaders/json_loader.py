"""
JSON file loader for Klovis.
Extracts text fields from JSON files into Document objects.
"""

from typing import List
from pathlib import Path
import json
from klovis.base import BaseLoader
from klovis.models import Document
from klovis.utils import get_logger

logger = get_logger(__name__)


class JSONLoader(BaseLoader):
    """
    Loads text data from JSON files.

    Parameters
    ----------
    text_field : str, optional
        JSON key to extract text from. Defaults to "content".
    """

    def __init__(self, path: str, text_field: str = "content"):
        self.path = Path(path)
        self.text_field = text_field
        logger.debug(f"JSONLoader initialized for {path} (text_field={text_field}).")

    def load(self) -> List[Document]:
        """
        Load text data from a JSON file.

        Returns
        -------
        List[Document]
            A list of extracted Document objects.
        """
        if not self.path.exists():
            raise FileNotFoundError(f"JSON file not found: {self.path}")

        documents: List[Document] = []

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))

            if isinstance(data, dict):
                text = str(data.get(self.text_field, "")).strip()
                if text:
                    documents.append(Document(source=str(self.path), content=text))

            elif isinstance(data, list):
                for i, item in enumerate(data):
                    text = str(item.get(self.text_field, "")).strip()
                    if text:
                        documents.append(Document(source=f"{self.path}#{i}", content=text))

            logger.debug(f"Loaded {len(documents)} document(s) from {self.path.name}")

        except json.JSONDecodeError:
            logger.error(f"Invalid JSON format: {self.path}")
        except Exception as e:
            logger.error(f"Unexpected error while reading {self.path}: {e}")

        return documents