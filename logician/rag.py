"""Simple RAG orchestrator.

This module demonstrates the retrieval + prompt assembly flow. It queries Qdrant for
similar vectors, then calls a local LLM or returns a simple assembled answer.
"""
from typing import List
import os
from .embedder import get_embedding
from .qdrant_wrapper import QdrantWrapper
import requests


class RagOrchestrator:
    def __init__(self, collection: str = "log_entries"):
        self.collection = collection
        self.qdrant = QdrantWrapper()
        self.llm_endpoint = os.getenv("LLM_ENDPOINT")
        self.llm_api_key = os.getenv("LLM_API_KEY")

    def retrieve(self, query: str, top_k: int = 3):
        vec = get_embedding(query)
        hits = self.qdrant.search(self.collection, vec, top_k=top_k)
        # Normalize hits for replacement when qdrant-client missing
        if not hits:
            return []
        return hits

    def call_llm(self, prompt: str) -> str:
        if self.llm_endpoint:
            try:
                resp = requests.post(
                    f"{self.llm_endpoint.rstrip('/')}/api/generate",
                    json={"prompt": prompt},
                    headers={"Authorization": f"Bearer {self.llm_api_key}"} if self.llm_api_key else {},
                    timeout=10,
                )
                resp.raise_for_status()
                data = resp.json()
                return data.get("text", "")
            except Exception:
                pass
        # fallback
        return "[LLM placeholder] Based on retrieved context: " + prompt[:200]

    def answer(self, query: str) -> str:
        hits = self.retrieve(query)
        context_texts = []
        for h in hits:
            # If using qdrant-client models, items are objects with payload and score
            if isinstance(h, dict):
                payload = h.get("payload") or h.get("payload", {})
                context_texts.append(str(payload))
            else:
                # Fallback string
                context_texts.append(str(h))

        prompt = f"User query:\n{query}\n\nRetrieved context:\n" + "\n---\n".join(context_texts)
        return self.call_llm(prompt)
