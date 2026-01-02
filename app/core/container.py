from app.repositories.history_repository import HistoryRepository, IHistoryRepository
from app.repositories.suggestion_repository import SuggestionRepository, ISuggestionRepository
from app.services.history_service import HistoryService, IHistoryService
from app.services.suggestion_service import ISuggestionService, SuggestionService

class Container:
    def __init__(self):
        # Repositorios
        self.suggestion_repository : ISuggestionRepository = SuggestionRepository()
        self.history_repository: IHistoryRepository = HistoryRepository()

        # Servicios
        self.suggestion_service : ISuggestionService = SuggestionService(self.suggestion_repository)
        self.history_service: IHistoryService = HistoryService(
            self.history_repository
        )
container = Container()