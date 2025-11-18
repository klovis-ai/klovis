"""
Exemple d'utilisation du KlovisPipeline.

Le pipeline orchestre toutes les étapes : loader -> cleaner -> chunker -> metadata
"""

from pathlib import Path
from klovis.pipeline import KlovisPipeline
from klovis.loaders import DirectoryLoader
from klovis.cleaning import (
    HTMLCleaner,
    TextCleaner,
    NormalizeCleaner,
    CompositeCleaner,
)
from klovis.chunking import SimpleChunker
from klovis.metadata.metadata_generator import MetadataGenerator


def example_basic_pipeline():
    """Exemple : Pipeline basique avec toutes les étapes."""
    print("=" * 60)
    print("🚀 KlovisPipeline - Pipeline complet")
    print("=" * 60)
    
    # Configuration du pipeline
    pipeline = KlovisPipeline(
        loader=DirectoryLoader(
            path="data/",
            recursive=True,
            markdownify=True,
        ),
        cleaner=CompositeCleaner([
            HTMLCleaner(),
            TextCleaner(),
            NormalizeCleaner(lowercase=True),
        ]),
        chunker=SimpleChunker(
            chunk_size=1000,
            chunk_overlap=100,
        ),
        metadata_generator=MetadataGenerator(),
        require_api_key=False,  # Pas besoin d'API key pour cet exemple
        export_results=True,  # Exporte les résultats en JSON
        export_dir="outputs",
        export_format="json",
    )
    
    # Exécuter le pipeline
    # Note: DirectoryLoader.load() ne prend pas d'arguments
    # Il faut charger manuellement puis passer au pipeline
    documents = pipeline.loader.load()
    results = pipeline.run(documents)
    
    print(f"✅ Pipeline terminé: {len(results)} chunk(s) généré(s)")
    print(f"📁 Résultats exportés dans: outputs/")
    print()


def example_pipeline_without_loader():
    """Exemple : Pipeline sans loader (documents déjà chargés)."""
    print("=" * 60)
    print("🚀 KlovisPipeline - Sans loader")
    print("=" * 60)
    
    from klovis.models import Document
    
    # Documents déjà chargés
    documents = [
        Document(source="doc1.txt", content="Content of document 1. " * 50),
        Document(source="doc2.txt", content="Content of document 2. " * 50),
    ]
    
    pipeline = KlovisPipeline(
        loader=None,  # Pas de loader
        cleaner=CompositeCleaner([TextCleaner(), NormalizeCleaner()]),
        chunker=SimpleChunker(chunk_size=500),
        require_api_key=False,
    )
    
    results = pipeline.run(documents)
    
    print(f"✅ {len(results)} chunk(s) généré(s) depuis {len(documents)} document(s)")
    print()


def example_pipeline_export_formats():
    """Exemple : Différents formats d'export."""
    print("=" * 60)
    print("📤 KlovisPipeline - Formats d'export")
    print("=" * 60)
    
    from klovis.models import Document
    
    documents = [
        Document(source="test.txt", content="Test content. " * 20),
    ]
    
    # Export JSON
    pipeline_json = KlovisPipeline(
        loader=None,
        chunker=SimpleChunker(chunk_size=500),
        export_results=True,
        export_format="json",
        require_api_key=False,
    )
    pipeline_json.run(documents)
    print("✅ Export JSON créé")
    
    # Export CSV
    pipeline_csv = KlovisPipeline(
        loader=None,
        chunker=SimpleChunker(chunk_size=500),
        export_results=True,
        export_format="csv",
        require_api_key=False,
    )
    pipeline_csv.run(documents)
    print("✅ Export CSV créé")
    
    # Export Parquet
    pipeline_parquet = KlovisPipeline(
        loader=None,
        chunker=SimpleChunker(chunk_size=500),
        export_results=True,
        export_format="parquet",
        require_api_key=False,
    )
    pipeline_parquet.run(documents)
    print("✅ Export Parquet créé")
    print()


if __name__ == "__main__":
    print("\n🚀 Exemples de KlovisPipeline\n")
    
    # Décommenter l'exemple que vous voulez tester
    # example_basic_pipeline()
    # example_pipeline_without_loader()
    # example_pipeline_export_formats()
    
    print("💡 Décommentez les exemples dans le code pour les tester !\n")
    print("📝 Note: Ajustez les chemins de fichiers selon votre environnement.\n")

