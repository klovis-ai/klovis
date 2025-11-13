"""
PDF Loader for Klovis.
Extracts text from PDFs, optionally formatting it in Markdown style.
"""

from pathlib import Path
from typing import List
import pdfplumber
from markdownify import markdownify as html_to_md
from klovis.models import Document
from klovis.utils import get_logger
from klovis.base import BaseLoader

logger = get_logger(__name__)


class PDFLoader(BaseLoader):
    """
    Loads and optionally Markdownifies PDF documents.

    Parameters
    ----------
    path : str
        Path to the PDF file or directory.
    markdownify : bool
        If True, adds Markdown structure for pages, titles, and spacing.
    """

    def __init__(self, path: str, markdownify: bool = False):
        self.path = Path(path)
        self.markdownify = markdownify
        logger.debug(f"PDFLoader initialized (markdownify={markdownify}).")

    def load(self) -> List[Document]:
        if not self.path.exists():
            raise FileNotFoundError(f"PDF path not found: {self.path}")

        documents = []

        if self.path.is_file():
            documents.append(self._load_file(self.path))
        else:
            for file_path in self.path.rglob("*.pdf"):
                documents.append(self._load_file(file_path))

        logger.info(f"Loaded {len(documents)} PDF document(s).")
        return documents

    def _load_file(self, file_path: Path) -> Document:
        logger.debug(f"Reading PDF: {file_path}")
        text_pages = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text() or ""
                    if self.markdownify:
                        # Simulate Markdown sections per page
                        text_pages.append(f"# Page {i}\n\n{text.strip()}\n\n---\n")
                    else:
                        text_pages.append(text)
        except Exception as e:
            logger.warning(f"Skipping unreadable PDF '{file_path}': {e}")
            return Document(
                source=str(file_path),
                content="",
                metadata={"pages": len(text_pages), "format": "markdown" if self.markdownify else "pdf"}
            )

        content = "\n".join(text_pages).strip()
        return Document(
            source=str(file_path),
            content=content,
            metadata={"pages": len(text_pages), "format": "markdown" if self.markdownify else "pdf"}
        )
