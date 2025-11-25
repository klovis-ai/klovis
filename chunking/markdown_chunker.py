import re
from typing import List, Optional, Tuple
try:
    from markdown_it import MarkdownIt
except ImportError:
    MarkdownIt = None  # type: ignore

from klovis.base import BaseChunker, BaseMerger
from klovis.models import Document, Chunk
from klovis.utils import get_logger

logger = get_logger(__name__)


class MarkdownChunker(BaseChunker):
    """
    Markdown Chunker:
    - Splits content by Markdown headings using an AST parser (markdown-it-py).
    - Produces base chunks without merging
    - If a merger is provided, delegates merging after local chunking
    """

    def __init__(
        self,
        max_chunk_size: int = 2000,
        overlap: int = 200,
        merger: Optional[BaseMerger] = None,
    ):
        if MarkdownIt is None:
            raise ImportError(
                "MarkdownChunker requires 'markdown-it-py' to be installed. "
                "Please run: pip install markdown-it-py"
            )

        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
        self.merger = merger
        self.md_parser = MarkdownIt()

        logger.debug(
            f"MarkdownChunker initialized (max_chunk_size={max_chunk_size}, "
            f"overlap={overlap}, merger={type(merger).__name__ if merger else 'None'})."
        )

    def chunk(self, documents: List[Document]) -> List[Chunk]:
        base_chunks: List[Chunk] = []

        for doc in documents:
            document_meta = doc.metadata or {}
            # Use the new AST-based splitter
            sections = self._split_by_markdown_titles(doc.content)
            
            chunk_id = 0
            buffer: List[str] = []
            current_size = 0

            for title, body in sections:
                section_text = (title + "\n" + body).strip()
                section_len = len(section_text)

                # If a section is too big → hard split only
                if section_len > self.max_chunk_size:
                    if buffer:
                        # flush buffer first
                        combined = "\n\n".join(buffer).strip()
                        base_chunks.append(
                            self._make_chunk(combined, doc.source, chunk_id, document_meta)
                        )
                        chunk_id += 1
                        buffer = []
                        current_size = 0

                    hard_chunks = self._hard_split(section_text, doc.source, chunk_id, document_meta)
                    base_chunks.extend(hard_chunks)
                    chunk_id += len(hard_chunks)
                    continue

                # Normal accumulation
                if current_size + section_len > self.max_chunk_size:
                    combined = "\n\n".join(buffer).strip()
                    base_chunks.append(
                        self._make_chunk(combined, doc.source, chunk_id, document_meta)
                    )
                    chunk_id += 1

                    # Overlap
                    overlap_text = combined[-self.overlap:] if self.overlap > 0 else ""
                    buffer = ([overlap_text] if overlap_text else []) + [section_text]
                    current_size = len(section_text) + len(overlap_text)

                else:
                    buffer.append(section_text)
                    current_size += section_len

            # Final flush
            if buffer:
                combined = "\n\n".join(buffer).strip()
                base_chunks.append(self._make_chunk(combined, doc.source, chunk_id, document_meta))

        logger.info(f"MarkdownChunker: produced {len(base_chunks)} base chunks.")

        if not self.merger:
            return base_chunks

        merged = self.merger.merge(chunks=base_chunks)
        logger.info(f"MarkdownChunker: merged into {len(merged)} chunks.")

        return merged

    def _split_by_markdown_titles(self, text: str) -> List[Tuple[str, str]]:
        """
        Splits markdown text by headings using AST parsing.
        Returns a list of (title, body) tuples.
        """
        tokens = self.md_parser.parse(text)
        
        # Find line numbers where headings start
        # tokens have .map = [start_line, end_line] (0-indexed)
        split_lines = []
        for token in tokens:
            if token.type == 'heading_open' and token.map:
                split_lines.append(token.map[0])
        
        split_lines = sorted(list(set(split_lines)))
        
        # If no headers found, return whole text
        if not split_lines:
            return [("# Section", text)]
            
        lines = text.splitlines(keepends=True)
        sections = []
        
        # Handle text before the first header
        if split_lines[0] > 0:
            pre_header_text = "".join(lines[:split_lines[0]]).strip()
            if pre_header_text:
                sections.append(("# Preamble", pre_header_text))
                
        # Slice text based on header positions
        for i, start_line in enumerate(split_lines):
            # End of this section is start of next section, or end of file
            next_start = split_lines[i+1] if i + 1 < len(split_lines) else len(lines)
            
            section_lines = lines[start_line:next_start]
            if not section_lines:
                continue
                
            # First line is the header
            title = section_lines[0].strip()
            
            # Rest is body
            body = "".join(section_lines[1:]).strip() if len(section_lines) > 1 else ""
            
            sections.append((title, body))
            
        return sections

    def _hard_split(
        self,
        text: str,
        source: str,
        start_id: int,
        document_meta: dict,
    ) -> List[Chunk]:

        chunks = []
        idx = start_id
        i = 0

        while i < len(text):
            end = i + self.max_chunk_size
            slice_text = text[i:end]

            chunks.append(
                self._make_chunk(
                    slice_text.strip(),
                    source,
                    idx,
                    document_meta,
                    ctype="markdown_hardsplit",
                )
            )

            i = end - self.overlap
            idx += 1

        return chunks

    def _make_chunk(self, text: str, source: str, chunk_id: int, document_meta: dict, ctype: str = "markdown") -> Chunk:
        metadata = {
            "chunk_id": chunk_id,
            "source": source,
            "length": len(text),
            "type": ctype,
        }
        for key, value in document_meta.items():
            metadata[f"doc_{key}"] = value
        return Chunk(text=text.strip(), metadata=metadata)
