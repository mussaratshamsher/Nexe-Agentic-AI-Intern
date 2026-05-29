from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class EmbeddingService:
    # Using a lightweight, high-performance model (free & local)
    _model = SentenceTransformer('all-MiniLM-L6-v2')

    @classmethod
    def get_embedding(cls, text: str) -> List[float]:
        """Generates a 384-dimension embedding for the given text."""
        embedding = cls._model.encode(text)
        return embedding.tolist()

    @classmethod
    def get_embeddings(cls, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of texts."""
        embeddings = cls._model.encode(texts)
        return embeddings.tolist()
