# Exemples Klovis

Ce dossier contient des exemples d'utilisation pour chaque module de Klovis.

## 📚 Liste des exemples

### 1. **example_loaders.py** - Chargement de documents
Exemples pour charger des documents depuis différentes sources :
- `DirectoryLoader` : Chargement récursif d'un répertoire
- `TextFileLoader` : Chargement de fichiers texte
- `HTMLLoader` : Chargement et conversion HTML
- `JSONLoader` : Chargement depuis JSON
- `PDFLoader` : Chargement de PDF

### 2. **example_cleaners.py** - Nettoyage de texte
Exemples pour nettoyer et normaliser le texte :
- `HTMLCleaner` : Nettoyage du HTML
- `TextCleaner` : Nettoyage des espaces et caractères spéciaux
- `NormalizeCleaner` : Normalisation (lowercase, unicode)
- `EmojiCleaner` : Gestion des emojis
- `CompositeCleaner` : Pipeline de nettoyage combiné

### 3. **example_chunkers.py** - Découpage en chunks
Exemples pour diviser les documents en chunks :
- `SimpleChunker` : Découpage par taille avec overlap
- `MarkdownChunker` : Découpage basé sur les titres Markdown
- `MarkdownChunker` avec `SemanticMerger` : Découpage + fusion sémantique

### 4. **example_merger.py** - Fusion sémantique
Exemples pour fusionner des chunks similaires :
- `SemanticMerger` : Fusion basée sur la similarité sémantique
- Utilisation avec différents embedders

### 5. **example_metadata.py** - Génération de métadonnées
Exemples pour enrichir les chunks avec des métadonnées :
- `MetadataGenerator` : Génération de métadonnées basiques
- Préservation des métadonnées existantes

### 6. **example_transformer.py** - Transformation de format
Exemples pour transformer les chunks en différents formats :
- `MarkdownTransformer` : Conversion en Markdown
- Avec ou sans métadonnées

### 7. **example_pipeline.py** - Pipeline complet
Exemples d'utilisation du `KlovisPipeline` :
- Pipeline basique avec toutes les étapes
- Pipeline sans loader
- Différents formats d'export (JSON, CSV, Parquet)

### 8. **example_complete_workflow.py** - Workflow de bout en bout
Exemple complet montrant toutes les étapes ensemble :
- Chargement → Nettoyage → Chunking → Métadonnées → Transformation
- Workflow avec `KlovisPipeline`

## 🚀 Comment utiliser

1. **Exécuter un exemple spécifique** :
```bash
python -m klovis.examples.example_loaders
python -m klovis.examples.example_cleaners
# etc.
```

2. **Ou importer dans votre code** :
```python
from klovis.examples.example_loaders import example_directory_loader
example_directory_loader()
```

3. **Décommenter les exemples** dans chaque fichier pour les tester.

## 📝 Notes

- Les exemples utilisent des données de test ou des chemins relatifs
- Ajustez les chemins de fichiers selon votre environnement
- Certains exemples nécessitent des dépendances externes (PDF, embeddings, etc.)
- Les exemples avec `SemanticMerger` nécessitent un embedder (voir `example_merger.py`)

## 🔧 Prérequis

Assurez-vous d'avoir installé toutes les dépendances :
```bash
pip install klovis
# Ou avec les dépendances optionnelles :
pip install klovis[all]
```

