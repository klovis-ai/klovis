# Integration Examples

Examples of integrating Klovis with other tools and frameworks.

## Vector Databases

### FAISS

```python
import faiss
import numpy as np
from klovis.loaders import DirectoryLoader
from klovis.chunking import SimpleChunker
from your_embedder import YourEmbedder

# Process documents with Klovis
loader = DirectoryLoader(path="data/")
documents = loader.load()

chunker = SimpleChunker(chunk_size=1000)
chunks = chunker.chunk(documents)

# Embed chunks
embedder = YourEmbedder()
embeddings = embedder.embed([chunk.text for chunk in chunks])

# Create FAISS index
dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Store chunk metadata
chunk_metadata = [chunk.to_dict() for chunk in chunks]

# Search
query_embedding = embedder.embed(["your query"])[0]
distances, indices = index.search(np.array([query_embedding]), k=5)
results = [chunks[i] for i in indices[0]]
```

### Chroma

```python
import chromadb
from klovis.loaders import DirectoryLoader
from klovis.chunking import SimpleChunker

# Process documents
loader = DirectoryLoader(path="data/")
documents = loader.load()

chunker = SimpleChunker(chunk_size=1000)
chunks = chunker.chunk(documents)

# Create Chroma collection
client = chromadb.Client()
collection = client.create_collection("documents")

# Add chunks to Chroma
for i, chunk in enumerate(chunks):
    collection.add(
        ids=[str(i)],
        documents=[chunk.text],
        metadatas=[chunk.metadata]
    )

# Query
results = collection.query(
    query_texts=["your query"],
    n_results=5
)
```

### Weaviate

```python
import weaviate
from klovis.loaders import DirectoryLoader
from klovis.chunking import SimpleChunker

# Process documents
loader = DirectoryLoader(path="data/")
documents = loader.load()

chunker = SimpleChunker(chunk_size=1000)
chunks = chunker.chunk(documents)

# Connect to Weaviate
client = weaviate.Client("http://localhost:8080")

# Create schema and add chunks
for chunk in chunks:
    client.data_object.create(
        data_object={
            "text": chunk.text,
            "source": chunk.metadata.get("source"),
        },
        class_name="Document"
    )
```

## LLM Frameworks

### OpenAI

```python
from openai import OpenAI
from klovis.loaders import DirectoryLoader
from klovis.chunking import SimpleChunker

# Process documents
loader = DirectoryLoader(path="data/")
documents = loader.load()

chunker = SimpleChunker(chunk_size=1000)
chunks = chunker.chunk(documents)

# Retrieve relevant chunks (using your vector DB)
relevant_chunks = retrieve_chunks(query, chunks)

# Build context
context = "\n\n".join([chunk.text for chunk in relevant_chunks])

# Generate with OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]
)
```

### LangChain

```python
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from klovis.loaders import DirectoryLoader
from klovis.chunking import SimpleChunker

# Process documents
loader = DirectoryLoader(path="data/")
documents = loader.load()

chunker = SimpleChunker(chunk_size=1000)
chunks = chunker.chunk(documents)

# Create LangChain documents
from langchain.schema import Document as LangChainDocument
langchain_docs = [
    LangChainDocument(page_content=chunk.text, metadata=chunk.metadata)
    for chunk in chunks
]

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(langchain_docs, embeddings)

# Query
results = vectorstore.similarity_search("your query", k=5)
```

## Data Processing

### Pandas

```python
import pandas as pd
from klovis.loaders import DirectoryLoader
from klovis.chunking import SimpleChunker

# Process documents
loader = DirectoryLoader(path="data/")
documents = loader.load()

chunker = SimpleChunker(chunk_size=1000)
chunks = chunker.chunk(documents)

# Convert to DataFrame
df = pd.DataFrame([
    {
        "chunk_id": chunk.metadata.get("chunk_id"),
        "source": chunk.metadata.get("source"),
        "text": chunk.text,
        "length": len(chunk.text),
    }
    for chunk in chunks
])

# Analyze
print(df.groupby("source").size())
print(df["length"].describe())
```

### Export to CSV/JSON

```python
import json
import csv
from klovis.loaders import DirectoryLoader
from klovis.chunking import SimpleChunker

# Process documents
loader = DirectoryLoader(path="data/")
documents = loader.load()

chunker = SimpleChunker(chunk_size=1000)
chunks = chunker.chunk(documents)

# Export to JSON
with open("chunks.json", "w") as f:
    json.dump([chunk.to_dict() for chunk in chunks], f, indent=2)

# Export to CSV
with open("chunks.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["chunk_id", "source", "text"])
    writer.writeheader()
    for chunk in chunks:
        writer.writerow({
            "chunk_id": chunk.metadata.get("chunk_id"),
            "source": chunk.metadata.get("source"),
            "text": chunk.text,
        })
```

## Workflow Orchestration

### Apache Airflow

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from klovis.loaders import DirectoryLoader
from klovis.chunking import SimpleChunker

def process_documents():
    loader = DirectoryLoader(path="data/")
    documents = loader.load()
    
    chunker = SimpleChunker(chunk_size=1000)
    chunks = chunker.chunk(documents)
    
    # Save results
    # ...

dag = DAG('klovis_pipeline', schedule_interval='@daily')

process_task = PythonOperator(
    task_id='process_documents',
    python_callable=process_documents,
    dag=dag
)
```

### Prefect

```python
from prefect import flow, task
from klovis.loaders import DirectoryLoader
from klovis.chunking import SimpleChunker

@task
def load_documents():
    loader = DirectoryLoader(path="data/")
    return loader.load()

@task
def chunk_documents(documents):
    chunker = SimpleChunker(chunk_size=1000)
    return chunker.chunk(documents)

@flow
def klovis_pipeline():
    documents = load_documents()
    chunks = chunk_documents(documents)
    return chunks

if __name__ == "__main__":
    klovis_pipeline()
```

## Best Practices

1. **Separate concerns**: Use Klovis for preprocessing, other tools for downstream tasks
2. **Preserve metadata**: Keep metadata for filtering and retrieval
3. **Standardize formats**: Use consistent chunk sizes and formats
4. **Handle errors**: Implement error handling for production use
5. **Monitor performance**: Track processing times and resource usage

