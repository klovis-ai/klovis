from klovis.utils import get_logger

logger = get_logger(__name__)


class EnrichedChunksPipeline:
    """
    Applies one or several enrichment generators to documents
    and returns NEW artificial chunks (enriched chunks).

    This does NOT modify the original documents.
    It simply appends extra chunks that contain enriched markdown.
    """

    def __init__(self, generators):
        self.generators = generators
        logger.debug(
            f"EnrichedChunksPipeline initialized with generators: "
            f"{[type(g).__name__ for g in generators]}"
        )

    def apply(self, documents):
        """
        Returns:
            A list of NEW Chunk objects (only enrichments, no originals).
        """
        enriched_chunks = []

        logger.info(f"EnrichedChunksPipeline: processing {len(documents)} document(s)...")

        for doc in documents:
            logger.debug(f"Enriching document: {doc.source}")

            for gen in self.generators:
                try:
                    new_chunks = gen.generate(doc)
                    if not new_chunks:
                        continue

                    enriched_chunks.extend(new_chunks)

                except Exception as e:
                    logger.error(
                        f"Generator {type(gen).__name__} failed for {doc.source}: {e}"
                    )

        logger.info(
            f"EnrichedChunksPipeline complete: {len(enriched_chunks)} enriched chunks generated."
        )

        return enriched_chunks
