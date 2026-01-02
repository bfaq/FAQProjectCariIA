from typing import Generic, TypeVar, List, Optional
from abc import ABC, abstractmethod

T = TypeVar('T')
class IRepository(ABC, Generic[T]):
    
    @abstractmethod
    def create(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        pass
    
    @abstractmethod
    def update(self, entity_id: int, entity: T) -> Optional[T]:
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        pass

class BaseRepository(Generic[T]):
    def __init__(self):
        self._items: List[T] = []
        self._next_id = 1
    
    def _generate_id(self) -> int:
        current_id = self._next_id
        self._next_id += 1
        return current_id