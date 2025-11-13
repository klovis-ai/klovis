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
    - Merges consecutive sections as long as the total length ≤ max_chunk_size
    """

    def __init__(self, max_chunk_size: int = 2000):
        self.max_chunk_size = max_chunk_size
        logger.debug(f"MarkdownChunker initialized (max_chunk_size={max_chunk_size}).")

    def chunk(self, documents: List[Document]) -> List[Chunk]:
        chunks: List[Chunk] = []
        for doc in documents:
            sections = self._split_by_markdown_titles(doc.content)
            chunk_id = 0

            buffer: List[str] = []
            current_size = 0

            for title, body in sections:
                section_text = (title + "\n" + body).strip()
                section_len = len(section_text)

                if buffer and current_size + section_len > self.max_chunk_size:
                    combined = "\n\n".join(buffer).strip()
                    chunks.append(self._make_chunk(combined, doc.source, chunk_id))
                    chunk_id += 1
                    buffer = [section_text]
                    current_size = section_len
                else:
                    buffer.append(section_text)
                    current_size += section_len

            if buffer:
                combined = "\n\n".join(buffer).strip()
                chunks.append(self._make_chunk(combined, doc.source, chunk_id))

        logger.info(f"MarkdownChunker: created {len(chunks)} chunks total.")
        return chunks

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
            if lines and re.match(r'^#{1,6}\s', lines[0]):
                title = lines[0].strip()
                body = "\n".join(lines[1:]).strip()
            else:
                title = "# Section"
                body = part

            sections.append((title, body))
        return sections

    def _make_chunk(self, text: str, source: str, chunk_id: int) -> Chunk:
        return Chunk(
            text=text.strip(),
            metadata={
                "chunk_id": chunk_id,
                "source": source,
                "length": len(text),
                "type": "markdown"
            },
        )
