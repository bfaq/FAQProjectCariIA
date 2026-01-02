from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.main import app
from app.repositories.suggestion_repository import SuggestionRepository
from app.services.suggestion_service import SuggestionService
from app.api.dependencies import get_suggestion_service


def override_get_suggestion_service():
    repository = SuggestionRepository()
    return SuggestionService(repository)


app.dependency_overrides[get_suggestion_service] = override_get_suggestion_service

client = TestClient(app)


def test_create_suggestion_success():
    payload = {
        "question": "¿Cómo elimino mi cuenta?",
        "suggestion": "Debes contactar al equipo de soporte."
    }

    response = client.post("/api/v1/suggestions/", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["question"] == payload["question"]
    assert body["suggestion"] == payload["suggestion"]
    assert "id" in body
    assert "created_at" in body


def test_create_suggestion_duplicate_question():
    payload = {
        "question": "¿Cómo cambio mi contraseña?",
        "suggestion": "Texto duplicado"
    }

    response = client.post("/api/v1/suggestions/", json=payload)

    assert response.status_code == 400

def test_update_suggestion_success():
    payload = {
        "question": "¿Cómo cambio mi contraseña?",
        "suggestion": "Respuesta actualizada"
    }

    response = client.put("/api/v1/suggestions/1", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["suggestion"] == "Respuesta actualizada"


def test_update_suggestion_not_found():
    payload = {
        "question": "Pregunta inexistente",
        "suggestion": "Respuesta"
    }

    response = client.put("/api/v1/suggestions/999", json=payload)

    assert response.status_code == 404


def test_delete_suggestion_success():
    response = client.delete("/api/v1/suggestions/2")

    assert response.status_code == 204


def test_delete_suggestion_not_found():
    response = client.delete("/api/v1/suggestions/999")

    assert response.status_code == 404


def test_suggest_success():
    payload = {
        "query": "como cambio mi contraseña"
    }

    response = client.post("/api/v1/suggestions/suggest", json=payload)

    assert response.status_code == 200
    body = response.json()

    assert "suggestion" in body
    assert "similarity_score" in body
    assert body["similarity_score"] > 0.4


def test_suggest_no_match():
    payload = {
        "query": "pregunta totalmente diferente sin sentido"
    }

    response = client.post("/api/v1/suggestions/suggest", json=payload)

    assert response.status_code == 200
    body = response.json()

    assert body["similarity_score"] == 0.0
    assert body["matched_question"] is None
