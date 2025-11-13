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
    Cleans text documents while preserving:
    - markdown structure
    - line breaks
    - URLs
    - markdown links

    Removes:
    - control characters
    - excessive spacing (without touching newlines)
    """

    URL_RE = re.compile(r"https?://[^\s)]+")
    MDLINK_RE = re.compile(r"\[[^\]]+\]\([^)]+\)")

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
            text = self.fix_punctuation(text)
            text = text.strip()
            if self.lowercase:
                text = text.lower()

            cleaned_docs.append(Document(source=doc.source, content=text))

        logger.info("Text cleaning completed successfully.")
        return cleaned_docs

    def fix_punctuation(self, text: str) -> str:
        """
        Fix punctuation spacing safely, without touching:
        - URLs
        - markdown links
        - markdown tables
        - markdown lists
        - headings
        """

        urls = {}
        def protect_url(match):
            token = f"§URL{len(urls)}§"
            urls[token] = match.group(0)
            return token

        text = self.URL_RE.sub(protect_url, text)

        mdlinks = {}
        def protect_mdlink(match):
            token = f"§MD{len(mdlinks)}§"
            mdlinks[token] = match.group(0)
            return token

        text = self.MDLINK_RE.sub(protect_mdlink, text)

        cleaned_lines = []
        for line in text.split("\n"):
            if line.lstrip().startswith(("#", "-", "*", ">")) or "|" in line:
                cleaned_lines.append(line)
                continue
            line = re.sub(r"\s*([.,!?;:])\s*", r"\1 ", line)
            line = re.sub(r" {2,}", " ", line)
            cleaned_lines.append(line.rstrip())

        text = "\n".join(cleaned_lines)
        for token, content in mdlinks.items():
            text = text.replace(token, content)
        for token, content in urls.items():
            text = text.replace(token, content)

        return text
