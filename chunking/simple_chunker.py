"""
Simple text chunker for Klovis.
Splits documents into overlapping text segments for RAG-ready processing.
"""

import re
from typing import List
from klovis.base import BaseChunker
from klovis.models import Document, Chunk
from klovis.utils import get_logger

logger = get_logger(__name__)


class SimpleChunker(BaseChunker):
    """
    Splits text documents into chunks of a given size with optional overlap.

    Parameters
    ----------
    chunk_size : int
        Maximum number of characters per chunk.
    chunk_overlap : int
        Number of characters to overlap between consecutive chunks.
    separators : list[str]
        Preferred separators for text splitting (ordered by priority).
    smart_overlap : bool
        If True, avoids cutting in the middle of a word for overlapping regions.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        separators: List[str] | None = None,
        smart_overlap: bool = True,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", "? ", "! ", "; "]
        self.smart_overlap = smart_overlap

        logger.debug(
            f"SimpleChunker initialized (chunk_size={chunk_size}, overlap={chunk_overlap}, "
            f"smart_overlap={smart_overlap})."
        )

    def chunk(self, documents: List[Chunk]) -> List[Chunk]:
        """
        Splits documents into smaller chunks.

        Returns
        -------
        List[Document]
            A list of chunked documents with 'chunk_id' in metadata.
        """
        chunked_docs: List[Chunk] = []
        logger.info(f"Chunking {len(documents)} document(s)...")

        for doc in documents:
            text = doc.content.strip()
            if not text:
                continue

            chunks = self._split_text(text)
            for i, chunk_text in enumerate(chunks):
                metadata = {"chunk_id": i, "source": doc.source, "length": len(chunk_text)}
                chunked_docs.append(
                    Chunk(
                        text=chunk_text.strip(),
                        metadata=metadata,
                    )
                )

        logger.info(f"Chunking completed: {len(chunked_docs)} total chunks.")
        return chunked_docs

    # --- Internal helpers ---
    def _split_text(self, text: str) -> List[str]:
        """
        Split text into chunks respecting preferred separators and overlap.
        """
        separator_regex = "|".join(map(re.escape, self.separators))
        parts = re.split(f"({separator_regex})", text)

        current_chunk = ""
        chunks: List[str] = []

        for part in parts:
            if len(current_chunk) + len(part) <= self.chunk_size:
                current_chunk += part
            else:
                chunks.append(current_chunk.strip())

                # Determine start of overlap
                overlap_start = max(len(current_chunk) - self.chunk_overlap, 0)

                # Smart overlap: avoid cutting in the middle of a word
                if self.smart_overlap:
                    while overlap_start > 0 and current_chunk[overlap_start] not in [" ", "\n", ".", "!", "?", ";", ":"]:
                        overlap_start -= 1

                current_chunk = current_chunk[overlap_start:] + part

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks
