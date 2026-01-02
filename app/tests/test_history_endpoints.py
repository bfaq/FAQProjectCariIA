from fastapi.testclient import TestClient
from app.main import app
from app.repositories.history_repository import HistoryRepository
from app.services.history_service import HistoryService
from app.api.dependencies import get_history_service


def override_get_history_service():
    repository = HistoryRepository()
    service = HistoryService(repository)

    service.save_query("Primera pregunta", "Respuesta 1", 0.8)
    service.save_query("Segunda pregunta", "Respuesta 2", 0.9)

    return service


app.dependency_overrides[get_history_service] = override_get_history_service

client = TestClient(app)


def test_get_history_endpoint_success():
    response = client.get("/api/v1/history/")

    assert response.status_code == 200
    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 2


def test_get_history_endpoint_order():
    response = client.get("/api/v1/history/")
    body = response.json()

    assert body[0]["query"] == "Segunda pregunta"
    assert body[1]["query"] == "Primera pregunta"


