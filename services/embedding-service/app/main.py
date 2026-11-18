from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from app.api.routes import health, models, embeddings
from app.core.config import settings
from app.services.model_loader import ModelLoader
from app.services.embedding_service import EmbeddingService


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

model_loader = ModelLoader()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s", settings.service_name)

    model_loader.load()

    app.state.model_loader = model_loader
    app.state.embedding_service = EmbeddingService(model_loader)

    logger.info("Embedding service initialized")

    yield

    logger.info("Stopping %s", settings.service_name)

    app.state.embedding_service = None
    app.state.model_loader = None


app = FastAPI(
    title="Embedding Service",
    description="Local multilingual text embedding service for AI agents",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(models.router)
app.include_router(embeddings.router)


@app.get("/")
async def root():
    return {
        "service": settings.service_name,
        "status": "running",
    }
