"""
Normalize cleaner for Klovis.
Standardizes punctuation, accents, and Unicode characters
to ensure consistent text formatting without breaking Markdown or URLs.
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
    Safe normalization preserving:
    - Markdown structure
    - URLs & Markdown links
    - Newlines (optional)
    """

    URL_RE = re.compile(r"https?://[^\s)]+")
    MDLINK_RE = re.compile(r"\[[^\]]+\]\([^)]+\)")

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

            # -----------------------
            # 0. Unicode normalization
            # -----------------------
            text = unicodedata.normalize("NFKC", text)

            # -----------------------
            # 1. Smart quotes & dashes
            # -----------------------
            replacements = {
                "“": '"', "”": '"', "«": '"', "»": '"',
                "‘": "'", "’": "'",
                "–": "-", "—": "-", "‐": "-",
                "…": "...",
            }
            for k, v in replacements.items():
                text = text.replace(k, v)

            # -----------------------
            # 2. Remove control chars EXCEPT newline
            # -----------------------
            text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", " ", text)

            # -----------------------
            # 3. Protect URLs & markdown links
            # -----------------------
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

            # -----------------------
            # 4. Safe punctuation cleaning per line
            # -----------------------
            cleaned_lines = []

            for line in text.split("\n"):

                # Do not alter markdown structural lines
                if (
                    line.lstrip().startswith(("#", "-", "*", "+", ">"))
                    or "|" in line  # markdown table
                ):
                    cleaned_lines.append(line)
                    continue

                # Normalize spaces around punctuation
                line = re.sub(r"\s*([.,!?;:])\s*", r"\1 ", line)

                # Remove repeated spaces
                line = re.sub(r" {2,}", " ", line)

                cleaned_lines.append(line.rstrip())

            text = "\n".join(cleaned_lines)

            # -----------------------
            # 5. Restore markdown links and URLs
            # -----------------------
            for token, v in mdlinks.items():
                text = text.replace(token, v)

            for token, v in urls.items():
                text = text.replace(token, v)

            # -----------------------
            # 6. Normalize whitespace
            # -----------------------
            if self.preserve_newlines:
                text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)
                text = re.sub(r"\n{3,}", "\n\n", text)
                text = re.sub(r" {2,}", " ", text)
            else:
                text = re.sub(r"\s+", " ", text)

            text = text.strip()

            # -----------------------
            # 7. Lowercase if needed
            # -----------------------
            if self.lowercase:
                text = text.lower()

            cleaned_docs.append(Document(source=doc.source, content=text))

        logger.info("NormalizeCleaner completed successfully.")
        return cleaned_docs
