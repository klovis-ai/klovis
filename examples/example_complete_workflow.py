"""
Exemple complet d'un workflow Klovis de bout en bout.

Cet exemple montre comment utiliser tous les composants ensemble
pour créer un pipeline complet de traitement de documents.
"""

from pathlib import Path
from klovis.pipeline import KlovisPipeline
from klovis.loaders import DirectoryLoader
from klovis.cleaning import (
    HTMLCleaner,
    TextCleaner,
    NormalizeCleaner,
    EmojiCleaner,
    CompositeCleaner,
)
from klovis.chunking import SimpleChunker, MarkdownChunker
from klovis.merger import SemanticMerger
from klovis.metadata.metadata_generator import MetadataGenerator
from klovis.transforming.markdown_transformer import MarkdownTransformer


def example_complete_workflow():
    """Exemple : Workflow complet de A à Z."""
    print("=" * 60)
    print("🎯 Workflow Complet Klovis")
    print("=" * 60)
    
    # =====================================================================
    # ÉTAPE 1: Configuration
    # =====================================================================
    data_dir = Path("data/")
    
    if not data_dir.exists():
        print(f"⚠️  Le dossier {data_dir} n'existe pas.")
        print("   Créez un dossier 'data/' avec vos fichiers pour tester.")
        return
    
    # =====================================================================
    # ÉTAPE 2: Chargement
    # =====================================================================
    print("\n📁 Étape 1: Chargement des documents...")
    loader = DirectoryLoader(
        path=str(data_dir),
        recursive=True,
        ignore_hidden=True,
        markdownify=True,  # Convertit HTML/PDF en Markdown
    )
    documents = loader.load()
    print(f"   ✅ {len(documents)} document(s) chargé(s)")
    
    # =====================================================================
    # ÉTAPE 3: Nettoyage
    # =====================================================================
    print("\n🧹 Étape 2: Nettoyage des documents...")
    cleaner = CompositeCleaner([
        HTMLCleaner(),  # Nettoie le HTML résiduel
        TextCleaner(),  # Nettoie les espaces et caractères spéciaux
        NormalizeCleaner(
            lowercase=True,  # Convertit en minuscules
            preserve_newlines=True,  # Préserve les sauts de ligne
        ),
        EmojiCleaner(replace=False),  # Supprime les emojis
    ])
    cleaned_docs = cleaner.clean(documents)
    print(f"   ✅ {len(cleaned_docs)} document(s) nettoyé(s)")
    
    # =====================================================================
    # ÉTAPE 4: Découpage (Chunking)
    # =====================================================================
    print("\n✂️  Étape 3: Découpage en chunks...")
    chunker = SimpleChunker(
        chunk_size=1000,  # 1000 caractères par chunk
        chunk_overlap=100,  # 100 caractères de chevauchement
        smart_overlap=True,  # Évite de couper au milieu d'un mot
    )
    chunks = chunker.chunk(cleaned_docs)
    print(f"   ✅ {len(chunks)} chunk(s) généré(s)")
    
    # =====================================================================
    # ÉTAPE 5: Fusion sémantique (optionnel)
    # =====================================================================
    print("\n🔗 Étape 4: Fusion sémantique (optionnel)...")
    print("   💡 Pour utiliser SemanticMerger, vous avez besoin d'un embedder:")
    print("      embedder = YourEmbedder()")
    print("      merger = SemanticMerger(embedder=embedder, max_size=2000)")
    print("      chunks = merger.merge(chunks)")
    # Décommentez pour utiliser:
    # embedder = YourEmbedder()
    # merger = SemanticMerger(embedder=embedder, max_size=2000)
    # chunks = merger.merge(chunks)
    
    # =====================================================================
    # ÉTAPE 6: Génération de métadonnées
    # =====================================================================
    print("\n📊 Étape 5: Génération de métadonnées...")
    metadata_gen = MetadataGenerator()
    enriched_chunks = metadata_gen.generate(chunks)
    print(f"   ✅ {len(enriched_chunks)} chunk(s) enrichi(s)")
    
    # =====================================================================
    # ÉTAPE 7: Transformation (optionnel)
    # =====================================================================
    print("\n📝 Étape 6: Transformation en Markdown (optionnel)...")
    transformer = MarkdownTransformer(include_metadata=True)
    markdown_chunks = transformer.transform(enriched_chunks)
    print(f"   ✅ {len(markdown_chunks)} chunk(s) transformé(s)")
    
    # =====================================================================
    # RÉSULTAT FINAL
    # =====================================================================
    print("\n" + "=" * 60)
    print("✅ Workflow terminé avec succès !")
    print("=" * 60)
    print(f"\n📊 Résumé:")
    print(f"   - Documents chargés: {len(documents)}")
    print(f"   - Chunks générés: {len(chunks)}")
    print(f"   - Chunks enrichis: {len(enriched_chunks)}")
    print(f"   - Chunks transformés: {len(markdown_chunks)}")
    print()
    
    # Afficher un exemple de chunk
    if enriched_chunks:
        print("📄 Exemple de chunk enrichi:")
        example = enriched_chunks[0]
        print(f"   Source: {example.metadata.get('source')}")
        print(f"   Chunk ID: {example.metadata.get('chunk_id')}")
        print(f"   Longueur: {example.metadata.get('length')} caractères")
        print(f"   Texte (premiers 100 caractères):")
        print(f"   {example.text[:100]}...")
    print()


def example_workflow_with_pipeline():
    """Exemple : Workflow utilisant KlovisPipeline."""
    print("=" * 60)
    print("🚀 Workflow avec KlovisPipeline")
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
        chunker=SimpleChunker(chunk_size=1000, chunk_overlap=100),
        metadata_generator=MetadataGenerator(),
        require_api_key=False,
        export_results=True,
        export_format="json",
    )
    
    # Exécution (DirectoryLoader nécessite un appel manuel)
    documents = pipeline.loader.load()
    results = pipeline.run(documents)
    
    print(f"✅ Pipeline exécuté: {len(results)} chunk(s) généré(s)")
    print(f"📁 Résultats exportés dans: outputs/")
    print()


if __name__ == "__main__":
    print("\n🎯 Exemples de Workflows Complets Klovis\n")
    
    # Décommenter l'exemple que vous voulez tester
    # example_complete_workflow()
    # example_workflow_with_pipeline()
    
    print("💡 Décommentez les exemples dans le code pour les tester !\n")
    print("📝 Note: Ajustez les chemins et configurations selon vos besoins.\n")

