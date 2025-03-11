"""
Embedding utilities for similarity calculation and deduplication
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from sentence_transformers import SentenceTransformer
from src.utils.config import get_config

# Global model instance
_model = None


def get_embedding_model() -> SentenceTransformer:
    """
    Get or initialize the embedding model

    Returns:
        SentenceTransformer: The embedding model
    """
    global _model
    if _model is None:
        config = get_config()
        model_name = config["EMBEDDING_MODEL"]
        _model = SentenceTransformer(model_name)
    return _model


def compute_embeddings(texts: List[str]) -> np.ndarray:
    """
    Compute embeddings for a list of texts

    Args:
        texts: List of texts to embed

    Returns:
        np.ndarray: Array of embeddings, shape (len(texts), embedding_dim)
    """
    model = get_embedding_model()
    return model.encode(texts, convert_to_numpy=True)


def compute_similarity(text1: str, text2: str) -> float:
    """
    Compute cosine similarity between two texts

    Args:
        text1: First text
        text2: Second text

    Returns:
        float: Cosine similarity (-1 to 1)
    """
    embeddings = compute_embeddings([text1, text2])
    vec1, vec2 = embeddings[0], embeddings[1]
    return cosine_similarity(vec1, vec2)


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        float: Cosine similarity (-1 to 1)
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)


def find_most_similar(query: str, candidates: List[str]) -> Tuple[int, float]:
    """
    Find the most similar text among candidates

    Args:
        query: Query text
        candidates: List of candidate texts

    Returns:
        Tuple[int, float]: Index of most similar candidate and similarity score
    """
    if not candidates:
        return -1, 0.0

    # Compute embeddings for query and all candidates
    all_texts = [query] + candidates
    embeddings = compute_embeddings(all_texts)

    query_embedding = embeddings[0]
    candidate_embeddings = embeddings[1:]

    # Compute similarities
    similarities = [
        cosine_similarity(query_embedding, candidate_embedding)
        for candidate_embedding in candidate_embeddings
    ]

    # Find most similar
    max_idx = int(np.argmax(similarities))
    max_similarity = similarities[max_idx]

    return max_idx, max_similarity


def is_duplicate(
    query: str, candidates: List[str], threshold: Optional[float] = None
) -> bool:
    """
    Check if a query is a duplicate of any candidates

    Args:
        query: Query text
        candidates: List of candidate texts
        threshold: Similarity threshold (if None, use config value)

    Returns:
        bool: True if query is a duplicate
    """
    if not candidates:
        return False

    if threshold is None:
        config = get_config()
        threshold = config["SIMILARITY_THRESHOLD"]

    _, similarity = find_most_similar(query, candidates)
    return similarity >= threshold
