"""
Markdown transformer for Klovis.
Formats documents into Markdown sections, one per Document.
"""

from typing import List, Dict
from klovis.models import Chunk
from klovis.transforming.base_transformer import BaseTransformer
from klovis.utils import get_logger

logger = get_logger(__name__)


class MarkdownTransformer(BaseTransformer):
    """
    Transforms each Document into a Markdown-formatted object.

    Returns a list of dictionaries:
    [
        {
            "source": "path/to/file",
            "chunk_id": 0,
            "markdown": "...",
        },
        ...
    ]
    """

    def __init__(self, include_metadata: bool = True):
        self.include_metadata = include_metadata
        logger.debug(f"MarkdownTransformer initialized (include_metadata={include_metadata}).")

    def transform(self, chunks: List[Chunk]) -> List[Dict]:
        logger.info(f"MarkdownTransformer: transforming {len(chunks)} document(s)...")
        results = []

        for chunk in chunks:
            lines = [f"## Source: `{chunk.metadata.get('source')}`\n"]

            if self.include_metadata and chunk.metadata:
                lines.append("**Metadata:**")
                for k, v in chunk.metadata.items():
                    lines.append(f"- **{k}**: {v}")
                lines.append("")

            lines.append("**Content:**\n")
            lines.append(chunk.text.strip())
            lines.append("\n---\n")

            results.append({
                "source": chunk.metadata.get("source"),
                "chunk_id": chunk.metadata.get("chunk_id"),
                "markdown": "\n".join(lines)
            })

        logger.info("Markdown transformation completed.")
        return results
