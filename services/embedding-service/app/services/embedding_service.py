import numpy as np

from app.core.config import settings
from app.services.model_loader import ModelLoader


class EmbeddingService:
    def __init__(self, model_loader: ModelLoader):
        self.model_loader = model_loader

    def generate_embeddings(self, texts: list[str]) -> tuple[list[list[float]], int]:
        if not texts:
            raise ValueError("Input texts cannot be empty")

        inputs = self.model_loader.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=settings.max_sequence_length,
            return_tensors="np",
        )

        model_inputs = {
            "input_ids": inputs["input_ids"].astype(np.int64),
            "attention_mask": inputs["attention_mask"].astype(np.int64),
        }

        outputs = self.model_loader.session.run(
            ["sentence_embedding"],
            model_inputs,
        )

        embeddings = outputs[0]

        if embeddings.shape != (len(texts), settings.model_dimension):
            raise RuntimeError(
                f"Unexpected embedding shape: {embeddings.shape}"
            )

        if not np.isfinite(embeddings).all():
            raise RuntimeError("Model returned non-finite embedding values")

        prompt_tokens = int(inputs["attention_mask"].sum())

        return embeddings.tolist(), prompt_tokens
