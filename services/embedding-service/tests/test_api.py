import pytest
from fastapi.testclient import TestClient

import app.main as main_module
from app.core.config import settings


class FakeEmbeddingService:
    """Mock service that does not load or execute the ONNX model."""

    def generate_embeddings(self, texts: list[str]):
        embeddings = [
            [0.1] * settings.model_dimension
            for _ in texts
        ]

        prompt_tokens = sum(len(text.split()) for text in texts)

        return embeddings, prompt_tokens


@pytest.fixture
def client(monkeypatch):
    # Prevent actual ONNX model loading during application startup.
    monkeypatch.setattr(
        main_module.model_loader,
        "load",
        lambda: None,
    )

    # Replace the real embedding service with a lightweight mock.
    monkeypatch.setattr(
        main_module,
        "EmbeddingService",
        lambda model_loader: FakeEmbeddingService(),
    )

    with TestClient(main_module.app) as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == settings.service_name


def test_list_models(client):
    response = client.get("/v1/models")

    assert response.status_code == 200

    result = response.json()

    assert result["object"] == "list"
    assert len(result["data"]) == 1
    assert result["data"][0]["id"] == settings.model_name
    assert result["data"][0]["dimension"] == settings.model_dimension


def test_create_single_embedding(client):
    response = client.post(
        "/v1/embeddings",
        json={
            "input": "Система долговременной памяти для ИИ-агентов.",
            "model": settings.model_name,
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert result["object"] == "list"
    assert result["model"] == settings.model_name
    assert len(result["data"]) == 1
    assert result["data"][0]["object"] == "embedding"
    assert result["data"][0]["index"] == 0
    assert len(result["data"][0]["embedding"]) == settings.model_dimension
    assert result["usage"]["prompt_tokens"] > 0
    assert result["usage"]["total_tokens"] == result["usage"]["prompt_tokens"]


def test_create_batch_embeddings(client):
    texts = [
        "Система долговременной памяти для ИИ-агентов.",
        "Long-term memory system for AI agents.",
    ]

    response = client.post(
        "/v1/embeddings",
        json={
            "input": texts,
            "model": settings.model_name,
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert len(result["data"]) == 2

    for index, item in enumerate(result["data"]):
        assert item["index"] == index
        assert item["object"] == "embedding"
        assert len(item["embedding"]) == settings.model_dimension

    assert result["usage"]["prompt_tokens"] > 0


def test_unknown_model_returns_404(client):
    response = client.post(
        "/v1/embeddings",
        json={
            "input": "Test text",
            "model": "unknown-model",
        },
    )

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.parametrize("text", ["", "   "])
def test_empty_input_returns_422(client, text):
    response = client.post(
        "/v1/embeddings",
        json={
            "input": text,
            "model": settings.model_name,
        },
    )

    assert response.status_code == 422


def test_empty_batch_returns_422(client):
    response = client.post(
        "/v1/embeddings",
        json={
            "input": [],
            "model": settings.model_name,
        },
    )

    assert response.status_code == 422


def test_invalid_json_returns_422(client):
    response = client.post(
        "/v1/embeddings",
        content="{invalid json",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
