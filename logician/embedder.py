"""Embedding generation wrapper.

This module provides a minimal function to generate embeddings using an HTTP LLM endpoint
or a local placeholder (random vectors) for testing.
"""
from typing import List
import os
import numpy as np
import requests


def get_embedding(text: str, model: str = None) -> List[float]:
    """Return an embedding vector for the given text.

    If LLM_ENDPOINT is set in env, send a request to the local LLM service that returns
    an embedding. Otherwise generate a deterministic pseudo-embedding using hashing.
    """
    endpoint = os.getenv("LLM_ENDPOINT")
    api_key = os.getenv("LLM_API_KEY")

    if endpoint:
        # Expect the local LLM service to expose an embeddings endpoint at /embeddings
        try:
            resp = requests.post(
                f"{endpoint.rstrip('/')}/api/embeddings",
                json={"input": text},
                timeout=10,
                headers={"Authorization": f"Bearer {api_key}"} if api_key else {},
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("embedding")
        except Exception:
            # fallback to deterministic pseudo-embedding
            pass

    # Deterministic pseudo-embedding for tests: use numpy hash to produce small vector
    rng = np.random.default_rng(abs(hash(text)) % (2 ** 32))
    vec = rng.standard_normal(128).astype(float).tolist()
    return vec
