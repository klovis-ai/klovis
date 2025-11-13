import re
from typing import List
from klovis.base import BaseChunker
from klovis.models import Document, Chunk
from klovis.utils import get_logger

logger = get_logger(__name__)


class MarkdownChunker(BaseChunker):
    """
    Markdown Chunker:
    - Splits content by Markdown headings (#, ##, ###...)
    - Merges consecutive sections while total length ≤ max_chunk_size
    - If a section is too large, hard-splits it into smaller chunks
    - Supports overlap between chunks
    """

    def __init__(self, max_chunk_size: int = 2000, overlap: int = 200):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
        logger.debug(
            f"MarkdownChunker initialized (max_chunk_size={max_chunk_size}, overlap={overlap})."
        )

    def chunk(self, documents: List[Document]) -> List[Chunk]:
        all_chunks: List[Chunk] = []

        for doc in documents:
            sections = self._split_by_markdown_titles(doc.content)
            chunk_id = 0
            buffer: List[str] = []
            current_size = 0

            for title, body in sections:
                section_text = (title + "\n" + body).strip()
                section_len = len(section_text)

                # Case 1: Section larger than max_chunk_size → hard split
                if section_len > self.max_chunk_size:
                    if buffer:
                        # flush buffer first
                        combined = "\n\n".join(buffer).strip()
                        all_chunks.append(
                            self._make_chunk(combined, doc.source, chunk_id)
                        )
                        chunk_id += 1
                        buffer = []
                        current_size = 0

                    hard_split_chunks = self._hard_split(section_text, doc.source, chunk_id)
                    all_chunks.extend(hard_split_chunks)
                    chunk_id += len(hard_split_chunks)
                    continue

                # Case 2: Normal merging
                if current_size + section_len > self.max_chunk_size:
                    combined = "\n\n".join(buffer).strip()
                    all_chunks.append(self._make_chunk(combined, doc.source, chunk_id))
                    chunk_id += 1

                    # Create overlap buffer
                    overlap_text = combined[-self.overlap:] if self.overlap > 0 else ""
                    buffer = ([overlap_text] if overlap_text else []) + [section_text]
                    current_size = len(section_text) + len(overlap_text)

                else:
                    buffer.append(section_text)
                    current_size += section_len

            # Final flush
            if buffer:
                combined = "\n\n".join(buffer).strip()
                all_chunks.append(self._make_chunk(combined, doc.source, chunk_id))

        logger.info(f"MarkdownChunker: created {len(all_chunks)} chunks total.")
        return all_chunks


    def _split_by_markdown_titles(self, text: str):
        """
        Splits the text based on Markdown headings.
        Returns a list of tuples (title, content).
        """
        parts = re.split(r'(?=^#{1,6}\s)', text, flags=re.MULTILINE)
        sections = []

        for part in parts:
            part = part.strip()
            if not part:
                continue

            lines = part.splitlines()
            if re.match(r'^#{1,6}\s', lines[0]):
                title = lines[0].strip()
                body = "\n".join(lines[1:]).strip()
            else:
                title = "# Section"
                body = part

            sections.append((title, body))

        return sections


    def _hard_split(self, text: str, source: str, start_id: int) -> List[Chunk]:
        """
        Splits a too-large section into max_chunk_size-sized chunks.
        Overlap also applied inside hard splits.
        """
        chunks = []
        i = 0
        idx = start_id

        while i < len(text):
            end = i + self.max_chunk_size
            piece = text[i:end]

            chunks.append(
                Chunk(
                    text=piece.strip(),
                    metadata={
                        "chunk_id": idx,
                        "source": source,
                        "length": len(piece),
                        "type": "markdown_hardsplit",
                    },
                )
            )

            
            i = end - self.overlap
            idx += 1

        return chunks


    def _make_chunk(self, text: str, source: str, chunk_id: int) -> Chunk:
        return Chunk(
            text=text.strip(),
            metadata={
                "chunk_id": chunk_id,
                "source": source,
                "length": len(text),
                "type": "markdown",
            },
        )
