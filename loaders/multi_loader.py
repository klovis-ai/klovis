"""
Multi-format file loader for Klovis.
Automatically selects the appropriate loader based on file extension.
"""

from typing import List, Dict
from pathlib import Path
from klovis.base import BaseLoader
from klovis.models import Document
from klovis.loaders.text_file_loader import TextFileLoader
from klovis.loaders.pdf_loader import PDFLoader
from klovis.loaders.json_loader import JSONLoader
from klovis.loaders.html_loader import HTMLLoader
from klovis.utils import get_logger

logger = get_logger(__name__)


class MultiLoader(BaseLoader):
    """
    Automatically dispatches file loading to the correct loader.

    Supported formats: TXT, PDF, JSON, HTML.
    """

    def __init__(self):
        self.loaders_map: Dict[str, BaseLoader] = {
            ".txt": TextFileLoader(),
            ".pdf": PDFLoader(),
            ".json": JSONLoader(),
            ".html": HTMLLoader(),
            ".htm": HTMLLoader(),
        }
        logger.debug(f"MultiLoader initialized with {len(self.loaders_map)} loaders.")

    def load(self, sources: List[str]) -> List[Document]:
        documents: List[Document] = []

        for src in sources:
            path = Path(src)
            ext = path.suffix.lower()

            if ext not in self.loaders_map:
                logger.warning(f"No loader available for file: {src}")
                continue

            loader = self.loaders_map[ext]
            try:
                docs = loader.load([src])
                documents.extend(docs)
            except Exception as e:
                logger.error(f"Failed to load {src}: {e}")

        logger.info(f"MultiLoader loaded {len(documents)} document(s) in total.")
        return documents
