from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["Models"])


@router.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": settings.model_name,
                "object": "model",
                "owned_by": "local",
                "dimension": settings.model_dimension,
            }
        ],
    }
