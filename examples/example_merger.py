"""
Exemple d'utilisation du SemanticMerger de Klovis.

Le SemanticMerger regroupe des chunks similaires sémantiquement
en utilisant des embeddings et du clustering.
"""

from klovis.models import Chunk
from klovis.merger import SemanticMerger


class MockEmbedder:
    """Mock embedder pour l'exemple (à remplacer par un vrai embedder)."""
    
    def __init__(self, dimension=384):
        self.dimension = dimension
    
    def embed(self, texts):
        """Retourne des embeddings aléatoires pour l'exemple."""
        import numpy as np
        return [np.random.rand(self.dimension).tolist() for _ in texts]


def example_semantic_merger():
    """Exemple : Fusion sémantique de chunks."""
    print("=" * 60)
    print("🔗 SemanticMerger - Fusion sémantique de chunks")
    print("=" * 60)
    
    # Créer des chunks similaires
    chunks = [
        Chunk(
            text="Python is a programming language. " * 10,
            metadata={"chunk_id": 0, "source": "doc1.txt"}
        ),
        Chunk(
            text="Python programming is great. " * 10,
            metadata={"chunk_id": 1, "source": "doc1.txt"}
        ),
        Chunk(
            text="JavaScript is also a programming language. " * 10,
            metadata={"chunk_id": 2, "source": "doc2.txt"}
        ),
        Chunk(
            text="Cooking recipes are fun. " * 10,
            metadata={"chunk_id": 3, "source": "doc3.txt"}
        ),
    ]
    
    print(f"📦 {len(chunks)} chunk(s) initial(aux)")
    
    # Créer un embedder mock (remplacer par un vrai embedder en production)
    embedder = MockEmbedder()
    
    # Créer le merger
    merger = SemanticMerger(
        embedder=embedder,
        max_size=1000,  # Taille max des chunks fusionnés
        batch_size=10,  # Taille des batches pour l'embedding
        distance_threshold=0.3,  # Seuil de distance pour le clustering
    )
    
    # Fusionner les chunks
    merged_chunks = merger.merge(chunks)
    
    print(f"✅ {len(merged_chunks)} chunk(s) fusionné(s)")
    print(f"\nChunks fusionnés:")
    for i, chunk in enumerate(merged_chunks):
        print(f"\n  Chunk {i+1}:")
        print(f"    Type: {chunk.metadata.get('type')}")
        print(f"    Taille: {len(chunk.text)} caractères")
        if 'n_merged_chunks' in chunk.metadata:
            print(f"    Chunks originaux fusionnés: {chunk.metadata['n_merged_chunks']}")
        print(f"    Texte (premiers 80 caractères): {chunk.text[:80]}...")
    print()


def example_semantic_merger_with_real_embedder():
    """Exemple : Utilisation avec un vrai embedder."""
    print("=" * 60)
    print("🔗 SemanticMerger avec embedder réel")
    print("=" * 60)
    
    print("💡 Pour utiliser avec un vrai embedder:")
    print("""
    from your_embedder import YourEmbedder
    
    embedder = YourEmbedder(model_name="your-model")
    merger = SemanticMerger(
        embedder=embedder,
        max_size=2000,
        batch_size=32,
        distance_threshold=0.3,  # Ajustez selon vos besoins
    )
    
    merged_chunks = merger.merge(chunks)
    """)
    print()


if __name__ == "__main__":
    print("\n🔗 Exemples de SemanticMerger Klovis\n")
    
    example_semantic_merger()
    example_semantic_merger_with_real_embedder()
    
    print("✅ Exemples de merger terminés !\n")
    print("💡 Note: Pour un usage réel, utilisez un embedder comme:")
    print("   - OpenAIEmbedder")
    print("   - SentenceTransformers (LocalEmbedder)")
    print("   - Ou tout autre embedder compatible\n")

