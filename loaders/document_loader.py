from typing import List, Any
from klovis.base import BaseLoader
from klovis.models import Document
from klovis.utils import get_logger

logger = get_logger(__name__)


class DocumentLoader(BaseLoader):
    """
    Loads raw documents and returns validated Document objects.
    """

    def load(self, sources: List[Any]) -> List[Document]:
        logger.debug(f"Loading {len(sources)} source(s)...")

        documents = [Document(source=src, content=f"Loaded content from {src}") for src in sources]

        logger.info(f"Loaded {len(documents)} document(s).")
        return documents
