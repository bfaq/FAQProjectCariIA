import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.suggestion_repository import SuggestionRepository
from app.services.suggestion_service import SuggestionService
from app.api.dependencies import get_suggestion_service

@pytest.fixture
def client():
    repository = SuggestionRepository()
    service = SuggestionService(repository)

    app.dependency_overrides[get_suggestion_service] = lambda: service

    yield TestClient(app)

    app.dependency_overrides.clear()
