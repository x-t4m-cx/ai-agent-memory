import logging

from fastapi import APIRouter, HTTPException, Request

from app.core.config import settings
from app.schemas.embeddings import (
    EmbeddingData,
    EmbeddingRequest,
    EmbeddingResponse,
    EmbeddingUsage,
)


logger = logging.getLogger(__name__)

router = APIRouter(tags=["Embeddings"])


@router.post(
    "/v1/embeddings",
    response_model=EmbeddingResponse,
)
async def create_embeddings(
    payload: EmbeddingRequest,
    request: Request,
):
    if payload.model and payload.model != settings.model_name:
        raise HTTPException(
            status_code=404,
            detail=f"Model '{payload.model}' not found",
        )

    embedding_service = getattr(
        request.app.state,
        "embedding_service",
        None,
    )

    if embedding_service is None:
        raise HTTPException(
            status_code=503,
            detail="Embedding model is not available",
        )

    try:
        texts = payload.get_texts()

        embeddings, prompt_tokens = (
            embedding_service.generate_embeddings(texts)
        )

        data = [
            EmbeddingData(
                embedding=embedding,
                index=index,
            )
            for index, embedding in enumerate(embeddings)
        ]

        return EmbeddingResponse(
            data=data,
            model=settings.model_name,
            usage=EmbeddingUsage(
                prompt_tokens=prompt_tokens,
                total_tokens=prompt_tokens,
            ),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        logger.exception("Embedding generation failed")

        raise HTTPException(
            status_code=500,
            detail="Embedding generation failed",
        ) from error
