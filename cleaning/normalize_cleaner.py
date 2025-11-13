"""
Normalize cleaner for Klovis.
Standardizes punctuation, accents, and Unicode characters
to ensure consistent text formatting.
"""

import re
import unicodedata
from typing import List
from klovis.base import BaseCleaner
from klovis.models import Document
from klovis.utils import get_logger

logger = get_logger(__name__)


class NormalizeCleaner(BaseCleaner):
    """
    Normalizes text by applying Unicode normalization, punctuation standardization,
    and whitespace consistency.

    Steps:
    - Normalize Unicode (NFKC)
    - Replace smart quotes and dashes
    - Remove non-printable symbols
    - Fix spacing around punctuation
    - Optionally lowercase
    - Optionally preserve paragraph/newline structure
    """

    def __init__(self, lowercase: bool = False, preserve_newlines: bool = True):
        self.lowercase = lowercase
        self.preserve_newlines = preserve_newlines
        logger.debug(
            f"NormalizeCleaner initialized (lowercase={lowercase}, preserve_newlines={preserve_newlines})."
        )

    def clean(self, documents: List[Document]) -> List[Document]:
        cleaned_docs: List[Document] = []
        logger.info(f"NormalizeCleaner: processing {len(documents)} document(s)...")

        for doc in documents:
            text = doc.content

            # Unicode normalization
            text = unicodedata.normalize("NFKC", text)

            # Replace smart quotes and dashes
            replacements = {
                "“": '"', "”": '"', "«": '"', "»": '"',
                "‘": "'", "’": "'",
                "–": "-", "—": "-", "‐": "-",
                "…": "...",
            }
            for k, v in replacements.items():
                text = text.replace(k, v)

            # Remove control chars
            text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", " ", text)

            # Fix spacing around punctuation
            text = re.sub(r"\s*([.,!?;:])\s*", r"\1 ", text)

            if self.preserve_newlines:
                text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)
                text = re.sub(r"\n{3,}", "\n\n", text)
                text = re.sub(r"[ ]{2,}", " ", text)
                text = text.strip()
            else:
                text = re.sub(r"\s+", " ", text).strip()

            # Lowercase optionnel
            if self.lowercase:
                text = text.lower()

            cleaned_docs.append(Document(source=doc.source, content=text))

        logger.info("NormalizeCleaner completed successfully.")
        return cleaned_docs
