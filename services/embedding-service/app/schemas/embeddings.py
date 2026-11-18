from typing import Literal

from pydantic import BaseModel, Field, model_validator


class EmbeddingRequest(BaseModel):
    input: str | list[str] = Field(
        description="Text or list of texts to generate embeddings for"
    )
    model: str | None = Field(
        default=None,
        description="Model identifier",
    )
    encoding_format: Literal["float"] = "float"

    @model_validator(mode="after")
    def validate_input(self):
        if isinstance(self.input, str):
            if not self.input.strip():
                raise ValueError("Input text cannot be empty")
        else:
            if not self.input:
                raise ValueError("Input list cannot be empty")

            if any(not text.strip() for text in self.input):
                raise ValueError("Input texts cannot be empty")

        return self

    def get_texts(self) -> list[str]:
        if isinstance(self.input, str):
            return [self.input]

        return self.input


class EmbeddingData(BaseModel):
    object: Literal["embedding"] = "embedding"
    embedding: list[float]
    index: int


class EmbeddingUsage(BaseModel):
    prompt_tokens: int
    total_tokens: int


class EmbeddingResponse(BaseModel):
    object: Literal["list"] = "list"
    data: list[EmbeddingData]
    model: str
    usage: EmbeddingUsage
