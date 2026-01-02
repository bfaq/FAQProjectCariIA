from typing import List, Optional
from abc import ABC, abstractmethod
from app.models.models import Suggestion
from app.repositories.base import IRepository
from datetime import date

class ISuggestionRepository(IRepository[Suggestion]):
    
    @abstractmethod
    def get_by_question(self, question: str) -> Optional[Suggestion]:
        pass

    @abstractmethod
    def get_all_questions(self) -> List[str]:
        pass

class SuggestionRepository(ISuggestionRepository):
  
  
    def __init__(self):
        super().__init__()
        self._items: List[Suggestion] = [
                Suggestion(1, "¿Cómo cambio mi contraseña?", "Puedes cambiar tu contraseña en la sección de   configuración de tu perfil.", created_at=date(2026, 1, 1)),
                Suggestion(2, "¿Cuál es el horario de atención?", "Nuestro horario es de lunes a viernes de 8 am a 5 pm.", created_at=date(2026, 1, 1))
        ]
        self._next_id = 3

    def create(self, suggestion: Suggestion) -> Suggestion:
        suggestion.id = self._next_id
        self._next_id += 1
        self._items.append(suggestion)
        return suggestion
    

    def get_by_id(self, suggestion_id: int) -> Optional[Suggestion]:
        return next((s for s in self._items if s.id == suggestion_id), None)

    def get_all(self) -> List[Suggestion]:
        return self._items.copy()

    def get_by_question(self, question: str) -> Optional[Suggestion]:
        return next((s for s in self._items if s.question.lower() == question.lower()), None)
    
    def get_all_questions(self) -> List[str]:
        return [s.question for s in self._items]

    def update(self, suggestion_id: int, updated_suggestion: Suggestion) -> Optional[Suggestion]:
        suggestion = self.get_by_id(suggestion_id)
        if suggestion:
            index = self._items.index(suggestion)
            updated_suggestion.id = suggestion_id
            self._items[index] = updated_suggestion
            return updated_suggestion
        return None
    
    def delete(self, suggestion_id: int) -> bool:
        suggestion = self.get_by_id(suggestion_id)
        if suggestion:
            self._items.remove(suggestion)
            return True
        return False