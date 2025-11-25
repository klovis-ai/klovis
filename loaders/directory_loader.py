"""
Directory Loader for Klovis.
Recursively loads supported document types using their respective loaders.
"""

from pathlib import Path
from typing import List, Iterator, Optional
import concurrent.futures
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
    Loads multiple document types from a directory structure in parallel.

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
    max_workers : int, optional
        Number of parallel workers for file loading. Defaults to None (CPU count).
    """

    SUPPORTED_EXTENSIONS = {".txt", ".html", ".htm", ".pdf", ".json"}

    def __init__(
        self,
        path: str,
        recursive: bool = True,
        ignore_hidden: bool = True,
        markdownify: bool = False,
        max_workers: Optional[int] = None,
    ):
        self.path = Path(path)
        self.recursive = recursive
        self.ignore_hidden = ignore_hidden
        self.markdownify = markdownify
        self.max_workers = max_workers

        logger.debug(
            f"DirectoryLoader initialized for {path} "
            f"(recursive={recursive}, ignore_hidden={ignore_hidden}, "
            f"markdownify={markdownify}, max_workers={max_workers})."
        )

    def load(self) -> List[Document]:
        """
        Load all documents from the directory in parallel.
        Blocks until all files are processed.
        """
        return list(self.load_stream())

    def load_stream(self) -> Iterator[Document]:
        """
        Load documents from the directory in parallel using a thread pool.
        Yields documents as they are processed.
        """
        if not self.path.exists():
            raise FileNotFoundError(f"Directory not found: {self.path}")

        files = self._get_files()
        logger.info(f"Found {len(files)} files to process in {self.path}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Map file paths to futures
            future_to_file = {
                executor.submit(self._load_single_file, f): f 
                for f in files
            }

            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    docs = future.result()
                    for doc in docs:
                        yield doc
                except Exception as e:
                    logger.error(f"Failed to process {file_path}: {e}")

    def _load_single_file(self, file_path: Path) -> List[Document]:
        """Helper method to load a single file, suitable for execution in a worker thread."""
        ext = file_path.suffix.lower()
        loader = None

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
                # This should be caught by _get_files filter, but safe double check
                return []
            
            # Load returns a list (or iterator converted to list by individual loaders for now)
            # We assume individual loaders are still synchronous for single files
            return list(loader.load())

        except Exception as e:
            logger.error(f"Error inside worker for {file_path}: {e}")
            raise e

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
