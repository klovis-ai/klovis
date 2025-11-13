"""
Text file loader for Klovis.
Reads plain text files (.txt) and returns validated Document objects.
"""

from typing import List
from pathlib import Path
from klovis.base import BaseLoader
from klovis.models import Document
from klovis.utils import get_logger

logger = get_logger(__name__)


class TextFileLoader(BaseLoader):
    """
    Loads plain text files into Pydantic Document objects.

    Parameters
    ----------
    encoding : str, optional
        Character encoding to use when reading files. Defaults to "utf-8".
    skip_empty : bool, optional
        Whether to skip empty files. Defaults to True.

    Raises
    ------
    FileNotFoundError
        If a specified file does not exist.
    ValueError
        If a file is empty (and skip_empty=False).
    """

    def __init__(self, path: str, encoding: str = "utf-8", skip_empty: bool = True):
        self.path = Path(path)
        self.encoding = encoding
        self.skip_empty = skip_empty
        logger.debug(f"TextFileLoader initialized for {path} (encoding={encoding}, skip_empty={skip_empty}).")

    def load(self) -> List[Document]:
        """
        Load a single .txt file and return it as a list of Document.
        """
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")

        try:
            content = self.path.read_text(encoding=self.encoding).strip()
            if not content and self.skip_empty:
                logger.debug(f"Skipped empty file: {self.path}")
                return []

            doc = Document(source=str(self.path), content=content)
            logger.debug(f"Loaded file: {self.path.name} ({len(content)} chars)")
            return [doc]

        except UnicodeDecodeError:
            logger.error(f"Encoding error reading file: {self.path} (encoding={self.encoding})")
            return []
        except Exception as e:
            logger.error(f"Unexpected error while loading {self.path}: {e}")
            return []
