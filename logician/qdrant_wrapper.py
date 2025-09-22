"""Minimal Qdrant client wrapper.

This wrapper uses qdrant-client when available. It provides simple helpers to
create a collection, upsert vectors, and search.
"""
from typing import List, Dict, Optional
import os


try:
    from qdrant_client import QdrantClient
    from qdrant_client.http.models import VectorParams, Distance
    _HAS_QDRANT = True
except Exception:
    QdrantClient = None  # type: ignore
    _HAS_QDRANT = False


class QdrantWrapper:
    def __init__(self, url: Optional[str] = None, api_key: Optional[str] = None):
        self.url = url or os.getenv("QDRANT_URL", "http://localhost:6333")
        self.api_key = api_key or os.getenv("QDRANT_API_KEY")
        if _HAS_QDRANT:
            self.client = QdrantClient(url=self.url, api_key=self.api_key)
        else:
            self.client = None

    def create_collection(self, name: str, vector_size: int = 128):
        if not _HAS_QDRANT:
            return
        params = VectorParams(size=vector_size, distance=Distance.COSINE)
        self.client.recreate_collection(collection_name=name, vectors_config=params)

    def upsert(self, collection: str, ids: List[str], vectors: List[List[float]], metadatas: List[Dict]):
        if not _HAS_QDRANT:
            return
        points = [{"id": i, "vector": v, "payload": m} for i, v, m in zip(ids, vectors, metadatas)]
        self.client.upsert(collection_name=collection, points=points)

    def search(self, collection: str, vector: List[float], top_k: int = 5):
        if not _HAS_QDRANT:
            return []
        results = self.client.search(collection_name=collection, query_vector=vector, limit=top_k)
        return results
