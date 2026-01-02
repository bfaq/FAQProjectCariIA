from typing import List
from abc import ABC, abstractmethod
from app.models.models import QueryHistory
from app.repositories.history_repository import IHistoryRepository

class IHistoryService(ABC):
   
    @abstractmethod
    def save_query(self, query: str, suggestion: str, score: float) -> QueryHistory:
        pass
    
    @abstractmethod
    def get_history(self) -> List[QueryHistory]:
        pass


class HistoryService(IHistoryService):
    
    def __init__(self, history_repository: IHistoryRepository):
        self.history_repo = history_repository
    
    def save_query(self, query: str, suggestion: str, score: float) -> QueryHistory:
        history = QueryHistory(
            id=0, 
            query=query,
            suggestion=suggestion,
            similarity_score=score
        )
        return self.history_repo.create(history)
    
    def get_history(self) -> List[QueryHistory]:
        return self.history_repo.get_all()
    
