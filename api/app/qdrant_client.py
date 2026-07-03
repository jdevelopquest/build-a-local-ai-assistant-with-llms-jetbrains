import uuid
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from api.app.config import settings
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self):
        self.url = settings.qdrant_url
        self.collection_name = settings.qdrant_collection
        self.client = None

    def connect(self):
        """Connect to Qdrant and ensure collection exists."""
        logger.info(f"Connecting to Qdrant at {self.url}")
        self.client = QdrantClient(url=self.url)

        # Check if collection exists, create if not
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]

        if self.collection_name not in collection_names:
            logger.info(f"Creating collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
        else:
            logger.info(f"Collection {self.collection_name} already exists")

    def add_documents(
        self, texts: List[str], vectors: List[List[float]], metadata: List[Dict[str, Any]]
    ):
        """Add documents with their vectors to the collection."""
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vec,
                payload={"text": text, **meta}
            )
            for text, vec, meta in zip(texts, vectors, metadata)
        ]

        self.client.upsert(collection_name=self.collection_name, points=points)
        logger.info(f"Added {len(points)} documents to {self.collection_name}")

    def search(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors."""
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
        ).points

        return [
            {
                "id": hit.id,
                "score": hit.score,
                "text": hit.payload.get("text", ""),
                "metadata": {k: v for k, v in hit.payload.items() if k != "text"},
            }
            for hit in results
        ]



# Global instance
vector_store = VectorStore()
