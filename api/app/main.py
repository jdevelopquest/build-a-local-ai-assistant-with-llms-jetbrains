from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response

import logging

from api.app.config import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

from api.app.routes import router
from api.app.embeddings import embedding_service
from api.app.qdrant_client import vector_store
from api.app.metrics import metrics
from api.app.ollama_client import OllamaClient

ollama_client = OllamaClient()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting AI Auto API")
    logger.info(f"Ollama URL: {settings.ollama_base_url}")
    logger.info(f"Qdrant URL: {settings.qdrant_url}")
    logger.info(f"Embedding Model: {settings.embedding_model}")

    # Load embedding model
    embedding_service.load()

    # Connect to Qdrant
    vector_store.connect()

    yield

    # Shutdown
    logger.info("Shutting down AI Auto API")


app = FastAPI(
    title="AI Auto API",
    description="OpenAI-compatible API with RAG capabilities",
    version="0.1.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(router)


@app.get("/health")
async def health_check():
    """
    Health check endpoint for container orchestration.
    Returns service status and configuration info.
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "ai-auto-api",
            "version": "0.1.0",
            "config": {
                "ollama_url": settings.ollama_base_url,
                "qdrant_url": settings.qdrant_url,
                "embedding_model": settings.embedding_model,
            },
        }
    )


@app.get("/metrics")
async def get_metrics():
    """
    Prometheus-compatible metrics endpoint.
    """
    return Response(
        content=metrics.get_prometheus_format(),
        media_type="text/plain",
    )
