from typing import List, Optional
from app.models.models import QueryHistory
from app.repositories.base import IRepository, BaseRepository

class IHistoryRepository(IRepository[QueryHistory]):
    pass


class HistoryRepository(IHistoryRepository, BaseRepository[QueryHistory]):
    
    def __init__(self):
        super().__init__()

    def create(self, history: QueryHistory) -> QueryHistory:
        history.id = self._generate_id()
        self._items.append(history)
        return history

    def get_by_id(self, history_id: int) -> Optional[QueryHistory]:
        return next((h for h in self._items if h.id == history_id), None)

    def get_all(self) -> List[QueryHistory]:
        # Devolver en orden inverso (más reciente primero)
        return sorted(self._items, key=lambda x: x.created_at, reverse=True)

    def update(self, history_id: int, updated_history: QueryHistory) -> Optional[QueryHistory]:
        history = self.get_by_id(history_id)
        if history:
            index = self._items.index(history)
            updated_history.id = history_id
            self._items[index] = updated_history
            return updated_history
        return None
    
    def delete(self, history_id: int) -> bool:
        history = self.get_by_id(history_id)
        if history:
            self._items.remove(history)
            return True
        return False