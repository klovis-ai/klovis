"""
Directory Loader for Klovis.
Recursively loads supported document types using their respective loaders.
"""

from pathlib import Path
from typing import List
from klovis.models import Document
from klovis.loaders.text_file_loader import TextFileLoader
from klovis.loaders.pdf_loader import PDFLoader
from klovis.loaders.html_loader import HTMLLoader
from klovis.loaders.json_loader import JSONLoader
from klovis.utils import get_logger
from klovis.base import BaseLoader

logger = get_logger(__name__)


class DirectoryLoader(BaseLoader):
    """
    Loads multiple document types from a directory structure.

    Parameters
    ----------
    path : str
        Path to the directory.
    recursive : bool
        If True, loads files from subdirectories recursively.
    ignore_hidden : bool
        If True, skips hidden files and directories.
    markdownify : bool
        If True, converts supported formats (HTML, PDF) into Markdown.
    """

    SUPPORTED_EXTENSIONS = {".txt", ".html", ".htm", ".pdf", ".json"}

    def __init__(
        self,
        path: str,
        recursive: bool = True,
        ignore_hidden: bool = True,
        markdownify: bool = False,
    ):
        self.path = Path(path)
        self.recursive = recursive
        self.ignore_hidden = ignore_hidden
        self.markdownify = markdownify

        logger.debug(
            f"DirectoryLoader initialized for {path} "
            f"(recursive={recursive}, ignore_hidden={ignore_hidden}, markdownify={markdownify})."
        )

    def load(self) -> List[Document]:
        if not self.path.exists():
            raise FileNotFoundError(f"Directory not found: {self.path}")

        documents: List[Document] = []
        files = self._get_files()

        for file_path in files:
            ext = file_path.suffix.lower()

            try:
                if ext == ".txt":
                    loader = TextFileLoader(str(file_path))
                elif ext in (".html", ".htm"):
                    loader = HTMLLoader(str(file_path), markdownify=self.markdownify)
                elif ext == ".pdf":
                    loader = PDFLoader(str(file_path), markdownify=self.markdownify)
                elif ext == ".json":
                    loader = JSONLoader(str(file_path))
                else:
                    logger.warning(f"Unsupported file format skipped: {file_path}")
                    continue

                docs = loader.load()
                documents.extend(docs)

            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")

        logger.info(f"Loaded {len(documents)} document(s) from directory.")
        return documents

    def _get_files(self) -> List[Path]:
        """Collect all supported files."""
        if self.recursive:
            files = [p for p in self.path.rglob("*") if p.is_file()]
        else:
            files = [p for p in self.path.glob("*") if p.is_file()]

        # Filter supported and visible files
        return [
            f for f in files
            if f.suffix.lower() in self.SUPPORTED_EXTENSIONS
            and not (self.ignore_hidden and f.name.startswith("."))
        ]
