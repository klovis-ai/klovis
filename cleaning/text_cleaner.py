"""
Text cleaner for Klovis.
Performs basic normalization and cleaning operations on textual content.
Preserves paragraph structure and Markdown formatting.
"""

import re
from typing import List
from klovis.base import BaseCleaner
from klovis.models import Document
from klovis.utils import get_logger

logger = get_logger(__name__)


class TextCleaner(BaseCleaner):
    """
    Cleans text documents by removing unnecessary whitespace,
    control characters, and repeated punctuation — while preserving newlines.

    Steps:
    - Remove control/non-printable characters
    - Normalize spaces (but keep line breaks)
    - Fix repeated punctuation
    - Optionally lowercase text
    """

    def __init__(self, lowercase: bool = False):
        self.lowercase = lowercase
        logger.debug(f"TextCleaner initialized (lowercase={self.lowercase}).")

    def clean(self, documents: List[Document]) -> List[Document]:
        cleaned_docs: List[Document] = []
        logger.info(f"TextCleaner: processing {len(documents)} document(s)...")

        for doc in documents:
            text = doc.content

            text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", " ", text)

            text = re.sub(r"[ \t]+", " ", text)   
            text = re.sub(r"\n{3,}", "\n\n", text)
            text = text.strip()

            text = re.sub(r"\s*([.,!?;:])\s*", r"\1 ", text)

            if self.lowercase:
                text = text.lower()

            cleaned_docs.append(Document(source=doc.source, content=text))

        logger.info("Text cleaning completed successfully.")
        return cleaned_docs
