from app.core.container import container
from app.services.suggestion_service import ISuggestionService
from app.services.history_service import IHistoryService

def get_suggestion_service() -> ISuggestionService:
    return container.suggestion_service

def get_history_service() -> IHistoryService:
    return container.history_service