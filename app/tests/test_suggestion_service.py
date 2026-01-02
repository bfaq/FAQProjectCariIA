import pytest
from app.services.suggestion_service import SuggestionService
from app.repositories.suggestion_repository import SuggestionRepository
from app.schemas.schemas import SuggestionCreate, SuggestionUpdate, QueryRequest
from app.core.exceptions import (
    AlreadyExistsError,
    NotFoundError,
    ServiceUnavailableError
)

@pytest.fixture
def repository():
    return SuggestionRepository()

@pytest.fixture
def service(repository):
    return SuggestionService(repository)

def test_create_suggestion_success(service):
    data = SuggestionCreate(
        question="¿Cómo creo un usuario?",
        suggestion="Desde el panel de administración"
    )

    result = service.create_suggestion(data)

    assert result.id is not None
    assert result.question == data.question
    assert result.suggestion == data.suggestion

def test_create_suggestion_duplicate_question(service):
    data = SuggestionCreate(
        question="¿Cómo cambio mi contraseña?",
        suggestion="Texto cualquiera"
    )

    with pytest.raises(AlreadyExistsError):
        service.create_suggestion(data)


def test_update_suggestion_success(service):
    update = SuggestionUpdate(
        suggestion="Nueva respuesta"
    )

    result = service.update_suggestion(1, update)

    assert result.suggestion == "Nueva respuesta"

def test_delete_suggestion_not_found(service):
    with pytest.raises(NotFoundError):
        service.delete_suggestion(999)
        
def test_get_suggestion_by_similarity(service):
    query = QueryRequest(query="Como cambio mi contraseña")

    response = service.get_suggestion(query)

    assert response.matched_question is not None
    assert response.similarity_score > 0.4
