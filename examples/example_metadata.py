"""
Exemples d'utilisation des générateurs de métadonnées de Klovis.

Les générateurs de métadonnées enrichissent les chunks avec des informations
supplémentaires (tags, longueur, etc.).
"""

from klovis.models import Chunk
from klovis.metadata.metadata_generator import MetadataGenerator


def example_metadata_generator():
    """Exemple : Génération de métadonnées basiques."""
    print("=" * 60)
    print("📊 MetadataGenerator - Génération de métadonnées")
    print("=" * 60)
    
    chunks = [
        Chunk(
            text="This is the first chunk with some content.",
            metadata={"chunk_id": 0, "source": "doc1.txt"}
        ),
        Chunk(
            text="This is the second chunk with different content.",
            metadata={"chunk_id": 1, "source": "doc1.txt"}
        ),
    ]
    
    generator = MetadataGenerator()
    enriched = generator.generate(chunks)
    
    print(f"✅ {len(enriched)} chunk(s) enrichi(s)")
    print(f"\nMétadonnées du premier chunk:")
    for key, value in enriched[0].metadata.items():
        print(f"  {key}: {value}")
    print()


def example_metadata_preservation():
    """Exemple : Préservation des métadonnées existantes."""
    print("=" * 60)
    print("💾 Préservation des métadonnées existantes")
    print("=" * 60)
    
    chunk = Chunk(
        text="Content with existing metadata.",
        metadata={
            "chunk_id": 0,
            "source": "doc.txt",
            "custom_field": "custom_value",
        }
    )
    
    generator = MetadataGenerator()
    enriched = generator.generate([chunk])
    
    print("Métadonnées avant enrichissement:")
    print(f"  {chunk.metadata}")
    print("\nMétadonnées après enrichissement:")
    print(f"  {enriched[0].metadata}")
    print("✅ Les métadonnées existantes sont préservées")
    print()


if __name__ == "__main__":
    print("\n📊 Exemples de générateurs de métadonnées Klovis\n")
    
    example_metadata_generator()
    example_metadata_preservation()
    
    print("✅ Tous les exemples de métadonnées ont été exécutés !\n")

