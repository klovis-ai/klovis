import numpy as np
from sklearn.cluster import AgglomerativeClustering
from typing import List
from klovis.models import Chunk
from klovis.base import BaseMerger
from klovis.utils import get_logger

logger = get_logger(__name__)


class SemanticMerger(BaseMerger):
    """
    Semantic clustering merger:
    - Embed chunks (batched)
    - Cluster embeddings semantically
    - Sort cluster members by similarity to cluster centroid
    - Merge into final chunks with max_size constraint
    """

    def __init__(
        self,
        embedder,
        max_size: int = 2000,
        batch_size: int = 10,
        n_clusters: int | None = None,
        distance_threshold: float | None = 0.1,
    ):
        self.embedder = embedder
        self.max_size = max_size
        self.batch_size = batch_size
        self.n_clusters = n_clusters
        self.distance_threshold = distance_threshold

        logger.debug(
            f"SemanticMerger initialized (max_size={max_size}, batch_size={batch_size}, "
            f"n_clusters={n_clusters}, distance_threshold={distance_threshold})."
        )

    def merge(self, chunks: List[Chunk]) -> List[Chunk]:
        logger.info(f"SemanticMerger: starting merge with {len(chunks)} chunk(s)...")
        texts = [c.text for c in chunks]

        logger.info("Embedding chunks in batches...")
        embeddings_result = self._embed_in_batches(texts)
        
        # Filter out failed embeddings (None values) and corresponding chunks
        valid_embeddings = []
        valid_chunks = []
        
        for idx, emb in enumerate(embeddings_result):
            if emb is not None:
                valid_embeddings.append(emb)
                valid_chunks.append(chunks[idx])
        
        if len(valid_embeddings) == 0:
            logger.error("No embeddings were successfully generated. Cannot proceed with clustering.")
            return []
        
        skipped_count = len(chunks) - len(valid_chunks)
        if skipped_count > 0:
            logger.warning(f"Skipping {skipped_count} chunk(s) that failed to embed.")
        
        embeddings = np.array(valid_embeddings)
        logger.info(f"Embedding completed: {len(embeddings)} vector(s) generated (out of {len(chunks)} chunks).")

        logger.info("Clustering embeddings...")
        cluster_labels = self._cluster_embeddings(embeddings)

        clusters = self._group_by_cluster(valid_chunks, embeddings, cluster_labels)
        n_clusters = len(clusters)
        logger.info(f"Clustering completed: {n_clusters} cluster(s) identified.")

        logger.info("Merging clusters into final chunks...")
        merged_chunks = self._merge_clusters(clusters)
        logger.info(f"SemanticMerger: merge completed → {len(merged_chunks)} final chunk(s).")

        return merged_chunks

    def _embed_in_batches(self, texts):
        all_vectors = []
        n_batches = (len(texts) + self.batch_size - 1) // self.batch_size
        logger.debug(f"Processing {len(texts)} text(s) in {n_batches} batch(es)...")
        
        failed_batches = 0
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            try:
                vectors = self.embedder.embed(batch)
                all_vectors.extend(vectors)
            except Exception as e:
                failed_batches += 1
                logger.warning(
                    f"Failed to embed batch {i // self.batch_size + 1}/{n_batches} "
                    f"(indices {i} to {min(i + self.batch_size, len(texts)) - 1}): {e}. "
                    f"Skipping this batch and continuing..."
                )
                # Add None to maintain alignment with texts for filtering later
                all_vectors.extend([None] * len(batch))
        
        if failed_batches > 0:
            successful_count = sum(1 for v in all_vectors if v is not None)
            logger.warning(
                f"Failed to embed {failed_batches} batch(es) out of {n_batches}. "
                f"Successfully embedded {successful_count} vector(s)."
            )
        
        return all_vectors


    def _cluster_embeddings(self, embeddings):
        logger.debug(
            f"Clustering {len(embeddings)} embedding(s) with "
            f"n_clusters={self.n_clusters}, distance_threshold={self.distance_threshold}..."
        )
        
        clustering = AgglomerativeClustering(
            n_clusters=self.n_clusters,
            distance_threshold=self.distance_threshold,
            metric="cosine",
            linkage="complete",
        )

        labels = clustering.fit_predict(embeddings)
        return labels


    def _group_by_cluster(self, chunks, embeddings, labels):
        clusters = {}

        for idx, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = {"chunks": [], "embeddings": []}
            clusters[label]["chunks"].append(chunks[idx])
            clusters[label]["embeddings"].append(embeddings[idx])

        return clusters


    def _merge_clusters(self, clusters):
        logger.debug(f"Merging {len(clusters)} cluster(s) with max_size={self.max_size}...")
        final_chunks = []
        chunk_id = 0

        for cluster_id, data in clusters.items():
            chunks_in_cluster = data["chunks"]
            embeds = np.array(data["embeddings"])

            centroid = embeds.mean(axis=0)

            similarities = embeds @ centroid / (
                np.linalg.norm(embeds, axis=1) * np.linalg.norm(centroid)
            )
            sorted_idx = np.argsort(-similarities)

            # Pre-compute all cluster chunks details (for all chunks in the cluster)
            cluster_all_chunks_details = []
            for idx in sorted_idx:
                chunk = chunks_in_cluster[idx]
                similarity_score = float(similarities[idx])
                cluster_all_chunks_details.append({
                    "chunk_id": chunk.metadata.get("chunk_id", idx),
                    "similarity": similarity_score,
                })
            
            cluster_all_similarity_scores = [item["similarity"] for item in cluster_all_chunks_details]
            n_cluster_chunks = len(cluster_all_chunks_details)

            buffer_texts = []
            buffer_chunks_with_scores = []
            size = 0
            cluster_chunk_index = 0  # Index of this final chunk within the cluster

            for idx in sorted_idx:
                chunk = chunks_in_cluster[idx]
                similarity_score = float(similarities[idx])
                
                if size + len(chunk.text) > self.max_size:
                    # Create metadata with count and detailed similarity scores
                    metadata = {
                        "chunk_id": chunk_id,
                        "type": "semantic",
                        "cluster_id": cluster_id,
                        "n_cluster_chunks": n_cluster_chunks,
                        "cluster_chunk_index": cluster_chunk_index,
                        "n_merged_chunks": len(buffer_chunks_with_scores),
                        "merged_chunks_details": buffer_chunks_with_scores.copy(),
                        "similarity_scores": [item["similarity"] for item in buffer_chunks_with_scores],
                        "cluster_all_chunks_details": cluster_all_chunks_details.copy(),
                        "cluster_all_similarity_scores": cluster_all_similarity_scores.copy(),
                    }
                    
                    final_chunks.append(
                        Chunk(
                            text="\n\n".join(buffer_texts),
                            metadata=metadata,
                        )
                    )
                    chunk_id += 1
                    cluster_chunk_index += 1
                    buffer_texts = []
                    buffer_chunks_with_scores = []
                    size = 0

                buffer_texts.append(chunk.text)
                buffer_chunks_with_scores.append({
                    "chunk_id": chunk.metadata.get("chunk_id", idx),
                    "similarity": similarity_score,
                })
                size += len(chunk.text)

            if buffer_texts:
                # Create metadata with count and detailed similarity scores
                metadata = {
                    "chunk_id": chunk_id,
                    "type": "semantic",
                    "cluster_id": cluster_id,
                    "n_cluster_chunks": n_cluster_chunks,
                    "cluster_chunk_index": cluster_chunk_index,
                    "n_merged_chunks": len(buffer_chunks_with_scores),
                    "merged_chunks_details": buffer_chunks_with_scores.copy(),
                    "similarity_scores": [item["similarity"] for item in buffer_chunks_with_scores],
                    "cluster_all_chunks_details": cluster_all_chunks_details.copy(),
                    "cluster_all_similarity_scores": cluster_all_similarity_scores.copy(),
                }
                
                final_chunks.append(
                    Chunk(
                        text="\n\n".join(buffer_texts),
                        metadata=metadata,
                    )
                )
                chunk_id += 1

        return final_chunks
