"""
Metadata module for Klovis.

Handles enrichment of data with metadata such as tags, Q/A pairs, or embeddings.
"""

from .pipeline import MetadataPipeline
from .generators.named_entities_generator import NamedEntitiesGenerator
from .generators.llm_metadata_generator import LLMMetadataGenerator
from .generators.enriched_chunks_generator import EnrichedChunksGenerator
from .enriched_chunks_pipeline import EnrichedChunksPipeline


__all__ = [
           "NamedEntitiesGenerator",
           "LLMMetadataGenerator",
           "MetadataPipeline",
           "EnrichedChunksGenerator",
           "EnrichedChunksPipeline" ]
