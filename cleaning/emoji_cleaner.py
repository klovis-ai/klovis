"""
Emoji cleaner for Klovis.
Removes or replaces emojis and pictographs to normalize text for NLP/RAG pipelines.
"""

import re
from typing import List
from klovis.base import BaseCleaner
from klovis.models import Document
from klovis.utils import get_logger
import unicodedata

logger = get_logger(__name__)


class EmojiCleaner(BaseCleaner):
    """
    Cleans emojis and pictographs from text content.

    Parameters
    ----------
    replace : bool, optional
        If True, replaces emojis with symbolic tags like [emoji_smile].
        If False, removes them entirely. Defaults to False.
    """

    def __init__(self, replace: bool = False):
        self.replace = replace
        logger.debug(f"EmojiCleaner initialized (replace={self.replace}).")

        # Comprehensive emoji pattern (Unicode ranges)
        self.emoji_pattern = re.compile(
            "[" +
            "\U0001F300-\U0001F5FF" +  # symbols & pictographs
            "\U0001F600-\U0001F64F" +  # emoticons
            "\U0001F680-\U0001F6FF" +  # transport & map
            "\U0001F700-\U0001F77F" +  # alchemical symbols
            "\U0001F780-\U0001F7FF" +  # geometric shapes extended
            "\U0001F800-\U0001F8FF" +  # supplemental arrows
            "\U0001F900-\U0001F9FF" +  # supplemental symbols
            "\U0001FA70-\U0001FAFF" +  # symbols & pictographs extended-A
            "\U00002700-\U000027BF" +  # dingbats
            "\U00002600-\U000026FF" +  # miscellaneous symbols
            "]+", flags=re.UNICODE
        )

    def clean(self, documents: List[Document]) -> List[Document]:
        cleaned_docs: List[Document] = []
        logger.info(f"EmojiCleaner: processing {len(documents)} document(s)...")

        for doc in documents:
            text = doc.content

            # Remove or replace emojis
            if self.replace:
                text = self.emoji_pattern.sub(self._emoji_to_token, text)
            else:
                text = self.emoji_pattern.sub("", text)


            text = re.sub(r"[ \t]+", " ", text)
            text = re.sub(r"\n{3,}", "\n\n", text)  # compactage léger des lignes vides
            text = text.strip()

            cleaned_docs.append(Document(source=doc.source, content=text))

        logger.info("Emoji cleaning completed successfully.")
        return cleaned_docs

    def _emoji_to_token(self, match: re.Match) -> str:
        """Convert emoji to a descriptive token like [emoji_heart]."""
        emoji_char = match.group(0)
        try:
            name = unicodedata.name(emoji_char).lower().replace(" ", "_")
            return f"[emoji_{name}]"
        except Exception:
            return "[emoji]"
