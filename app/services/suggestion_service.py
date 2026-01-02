import difflib
from typing import List, Optional, Tuple
from abc import ABC, abstractmethod
from app.models.models import Suggestion
from app.repositories.suggestion_repository import ISuggestionRepository
from app.schemas.schemas import QueryRequest, QueryResponse, SuggestionCreate, SuggestionUpdate, SuggestionBase
from app.core.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    ServiceUnavailableError,
    DomainError
)

class ISuggestionService(ABC):
  
    @abstractmethod
    def get_suggestion(self, query_request: QueryRequest) -> QueryResponse:
        pass

    @abstractmethod
    def get_all_suggestions(self) -> List[Suggestion]:
        pass

    @abstractmethod
    def create_suggestion(self, suggestion_data: SuggestionCreate) -> Suggestion:
        pass

    @abstractmethod
    def get_suggestion_by_id(self, suggestion_id: int) -> Suggestion:
        pass

    @abstractmethod
    def update_suggestion(self, suggestion_id: int, suggestion_data: SuggestionUpdate) -> Suggestion:
        pass

    @abstractmethod
    def delete_suggestion(self, suggestion_id: int) -> None:
        pass

class SuggestionService(ISuggestionService):

    def __init__(self, repositorysitory: ISuggestionRepository, threshold: float = 0.4):
        self.repository = repositorysitory
        self.threshold = threshold


    def create_suggestion(self, suggestion_data: SuggestionCreate) -> Suggestion:
        existing = self.repository.get_by_question(suggestion_data.question)
        if existing:
            raise AlreadyExistsError("La pregunta ya está registrada")

        
        suggestion = Suggestion(
            id=0,
            question=suggestion_data.question,
            suggestion=suggestion_data.suggestion
        )
        return self.repository.create(suggestion)

    def get_all_suggestions(self) -> List[Suggestion]:
        return self.repository.get_all()
    
    def get_suggestion_by_id(self, suggestion_id: int) -> Suggestion:
        suggestion = self.repository.get_by_id(suggestion_id)
        if not suggestion:
            raise NotFoundError("Sugerencia no encontrada")
        return suggestion

    def update_suggestion(self, suggestion_id: int, suggestion_data: SuggestionUpdate) -> Suggestion:
        suggestion = self.get_suggestion_by_id(suggestion_id)
        
        if suggestion_data.suggestion is not None:
            suggestion.suggestion = suggestion_data.suggestion
        if suggestion_data.question is not None:
            existing = self.repository.get_by_question(suggestion_data.question)
            if existing and existing.id != suggestion_id:
                raise AlreadyExistsError("La pregunta ya está registrada")

            suggestion.question = suggestion_data.question

        return self.repository.update(suggestion_id, suggestion)

    def delete_suggestion(self, suggestion_id: int) -> None:
        if not self.repository.delete(suggestion_id):
            raise NotFoundError("Sugerencia no encontrada")

    def get_suggestion(self, query_request: QueryRequest) -> QueryResponse:
        """
        Busca una sugerencia basada en la consulta del usuario.
        Guarda la consulta en el historial.
        """
        query = query_request.query
        
        # Obtener todas las preguntas de la base de conocimiento
        all_questions = self.repository.get_all_questions()
        
        if not all_questions:
            raise ServiceUnavailableError("Base de conocimiento vacía")

        
        # Buscar la mejor coincidencia
        match_result = self.find_best_match(query, all_questions)
        
          
        if not match_result:
            # No se encontró coincidencia suficiente
            return QueryResponse(
                suggestion="Lo siento, no encontré una respuesta similar a tu pregunta. Por favor, contacta con soporte.",
                similarity_score=0.0,
                matched_question=None
            )
        
        matched_question, similarity_score = match_result
        
        # Obtener la sugerencia correspondiente
        suggestion = self.repository.get_by_question(matched_question)
        
        if not suggestion:
           raise NotFoundError("Sugerencia no encontrada")
           
        return QueryResponse(
            suggestion=suggestion.suggestion,
            similarity_score=round(similarity_score, 2),
            matched_question=matched_question
        )
    
    ## Métodos de búsqueda y similitud de texto ##
    
    def find_best_match(self, query: str, candidates: List[str]) -> Optional[Tuple[str, float]]:
        """
        Encuentra la mejor coincidencia para una consulta.
        
        Args:
            query: Texto de consulta del usuario
            candidates: Lista de textos candidatos
            
        Returns:
            Tupla (mejor_coincidencia, puntuación) o None si no hay coincidencias
        """
        if not candidates:
            return None
        
        query_normalized = query.lower().strip()
        candidates_normalized = [c.lower().strip() for c in candidates]
        
        matches = difflib.get_close_matches(
            query_normalized,
            candidates_normalized,
            n=1,
            cutoff=self.threshold
        )
        
        if not matches:
            return None
        
        best_match_normalized = matches[0]
        best_match_index = candidates_normalized.index(best_match_normalized)
        best_match_original = candidates[best_match_index]
        
        similarity_score = difflib.SequenceMatcher(
            None,
            query_normalized,
            best_match_normalized
        ).ratio()
        
        return best_match_original, similarity_score
    
