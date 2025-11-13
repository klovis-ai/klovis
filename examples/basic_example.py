"""
Basic example demonstrating how to use Klovis modules both individually
and through the unified KlovisPipeline.

Run this script after setting your KLOVIS_API_KEY in a `.env` file.
"""

from klovis.loaders import DocumentLoader
from klovis.extraction import VLExtractor
from klovis.cleaning import TextCleaner
from klovis.chunking import SimpleChunker
from klovis.metadata import MetadataGenerator
from klovis.pipeline import KlovisPipeline


def manual_usage():
    """Example showing manual, step-by-step use of individual modules."""

    print("=== Manual Module Usage ===")

    loader = DocumentLoader()
    extractor = VLExtractor()
    cleaner = TextCleaner()
    chunker = SimpleChunker()
    meta = MetadataGenerator()

    data = loader.load(["example_document.txt"])
    data = extractor.extract(data)
    data = cleaner.clean(data)
    chunks = chunker.chunk(data)
    results = meta.generate(chunks)

    print(f"Processed {len(results)} chunks.")
    print("Sample output:", results[0])


def pipeline_usage():
    """Example showing automatic pipeline-based processing."""

    print("\n=== Pipeline Usage ===")

    pipeline = KlovisPipeline(
        loader=DocumentLoader(),
        extractor=VLExtractor(),
        cleaner=TextCleaner(),
        chunker=SimpleChunker(),
        metadata_generator=MetadataGenerator(),
    )

    results = pipeline.run(["example_document.txt"])
    print(f"Pipeline produced {len(results)} results.")
    print("Sample output:", results[0])


if __name__ == "__main__":
    manual_usage()
    pipeline_usage()
