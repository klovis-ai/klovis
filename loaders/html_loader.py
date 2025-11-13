"""
HTML Loader for Klovis.
Extracts content from HTML files, optionally converting it to Markdown.
"""

from pathlib import Path
from typing import List
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_md
from klovis.models import Document
from klovis.utils import get_logger
from klovis.base import BaseLoader

logger = get_logger(__name__)


class HTMLLoader(BaseLoader):
    """
    Loads HTML files from disk, with optional Markdown conversion.

    Parameters
    ----------
    path : str
        Path to the HTML file or directory.
    markdownify : bool
        If True, converts HTML to Markdown format.
    """

    def __init__(self, path: str, markdownify: bool = False):
        self.path = Path(path)
        self.markdownify = markdownify
        logger.debug(f"HTMLLoader initialized (markdownify={markdownify}).")

    def load(self) -> List[Document]:
        if not self.path.exists():
            raise FileNotFoundError(f"HTML path not found: {self.path}")

        documents = []

        if self.path.is_file():
            documents.append(self._load_file(self.path))
        else:
            for file_path in self.path.rglob("*.html"):
                documents.append(self._load_file(file_path))

        logger.info(f"Loaded {len(documents)} HTML document(s).")
        return documents

    def _load_file(self, file_path: Path) -> Document:
        logger.debug(f"Reading HTML file: {file_path}")
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")

        # Remove scripts and style elements
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        text_content = soup.get_text(separator="\n")

        # Optionally convert to Markdown
        if self.markdownify:
            markdown = html_to_md(html_content, heading_style="ATX")
            content = markdown.strip()
        else:
            content = text_content.strip()

        return Document(
            source=str(file_path),
            content=content,
            metadata={"format": "markdown" if self.markdownify else "html"}
        )
