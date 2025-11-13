"""
HTML cleaner for Klovis.
Removes HTML tags while preserving paragraph and structural line breaks.
"""

import re
import html
from bs4 import BeautifulSoup
from typing import List
from klovis.base import BaseCleaner
from klovis.models import Document
from klovis.utils import get_logger

logger = get_logger(__name__)


class HTMLCleaner(BaseCleaner):
    """
    Cleans HTML content while preserving structural newlines.
    Converts HTML entities and removes invisible characters.

    Parameters
    ----------
    strip_whitespace : bool, optional
        Whether to normalize excessive spaces (default: True).
    """

    def __init__(self, strip_whitespace: bool = True):
        self.strip_whitespace = strip_whitespace
        logger.debug(f"HTMLCleaner initialized (strip_whitespace={strip_whitespace}).")

    def clean(self, documents: List[Document]) -> List[Document]:
        cleaned_docs: List[Document] = []
        logger.info(f"HTMLCleaner: processing {len(documents)} document(s)...")

        for doc in documents:
            text = doc.content

            # 1️⃣ Parse HTML and extract text with logical line breaks
            soup = BeautifulSoup(text, "html.parser")
            text = soup.get_text(separator="\n")  
            # 2️⃣ Decode HTML entities (e.g. &nbsp;, &amp;, &#39;)
            text = html.unescape(text)

            # 3️⃣ Remove invisible non-breaking spaces and zero-width chars
            text = text.replace("\xa0", " ")  # non-breaking space
            text = re.sub(r"[\u200B-\u200D\uFEFF]", "", text)

            # 4️⃣ Normalize line spacing
            # Remplace plusieurs retours vides par deux max
            text = re.sub(r"\n{3,}", "\n\n", text)

            # 5️⃣ Optionnel : nettoyage d'espaces multiples dans les lignes
            if self.strip_whitespace:
                text = re.sub(r"[ \t]+", " ", text)
                # Supprime les espaces autour des sauts de ligne
                text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)
                text = text.strip()

            cleaned_docs.append(Document(source=doc.source, content=text))

        logger.info("HTML cleaning completed successfully.")
        return cleaned_docs
