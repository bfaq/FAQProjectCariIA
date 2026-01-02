from app.services.history_service import HistoryService
from app.repositories.history_repository import HistoryRepository


def test_save_query_success():
    repository = HistoryRepository()
    service = HistoryService(repository)

    result = service.save_query(
        query="¿Cómo cambio mi contraseña?",
        suggestion="Desde configuración",
        score=0.95
    )

    assert result.id is not None
    assert result.query == "¿Cómo cambio mi contraseña?"
    assert result.suggestion == "Desde configuración"
    assert result.similarity_score == 0.95


def test_get_history_returns_list():
    repository = HistoryRepository()
    service = HistoryService(repository)

    service.save_query("Q1", "S1", 0.8)
    service.save_query("Q2", "S2", 0.9)

    history = service.get_history()

    assert isinstance(history, list)
    assert len(history) == 2


def test_get_history_ordered_by_most_recent():
    repository = HistoryRepository()
    service = HistoryService(repository)

    first = service.save_query("Primera", "Respuesta 1", 0.7)
    second = service.save_query("Segunda", "Respuesta 2", 0.9)

    history = service.get_history()

    assert history[0].id == second.id
    assert history[1].id == first.id
