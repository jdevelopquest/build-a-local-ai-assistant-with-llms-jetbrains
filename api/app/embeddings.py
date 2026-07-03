from typing import List
from sentence_transformers import SentenceTransformer

from api.app.config import settings

import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        self.model_name = settings.embedding_model
        self.device = settings.embedding_device
        self.model = None

    def load(self):
        """Load the embedding model."""
        logger.info(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name, device=self.device)
        logger.info(f"Embedding model loaded on {self.device}")

    def encode(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load() first.")

        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()


# Global instance
embedding_service = EmbeddingService()
