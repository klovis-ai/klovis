from typing import List
from klovis.base import BaseMetadataGenerator
from klovis.models import Chunk
from klovis.utils import get_logger

logger = get_logger(__name__)


class MetadataGenerator(BaseMetadataGenerator):
    """
    Generates metadata for each Chunk object.
    """

    def generate(self, chunks: List[Chunk]) -> List[Chunk]:
        logger.debug(f"Generating metadata for {len(chunks)} chunk(s)...")

        enriched_chunks = []
        for chunk in chunks:
            enriched_chunk = chunk.model_copy(update={
                "metadata": {
                    "length": len(chunk.text),
                    "tags": ["example"]
                }
            })
            enriched_chunks.append(enriched_chunk)

        logger.info("Metadata generation completed.")
        return enriched_chunks
