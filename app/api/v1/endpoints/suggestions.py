from typing import List
from fastapi import APIRouter, Depends, status
from app.schemas.schemas import QueryRequest, QueryResponse, SuggestionCreate, SuggestionUpdate, SuggestionResponse
from app.services.suggestion_service import ISuggestionService
from app.services.history_service import IHistoryService
from app.api.dependencies import get_suggestion_service, get_history_service

router = APIRouter()

@router.post("/", response_model=SuggestionResponse, status_code=status.HTTP_201_CREATED)
async def create_suggestion(
    suggestion: SuggestionCreate,
    suggestion_service: ISuggestionService = Depends(get_suggestion_service),
):
    return suggestion_service.create_suggestion(suggestion)

@router.get("/", response_model=List[SuggestionResponse])
async def get_suggestions(
    suggestion_service: ISuggestionService = Depends(get_suggestion_service)
):
    return suggestion_service.get_all_suggestions()

@router.put("/{suggestion_id}", response_model=SuggestionResponse)
async def update_suggestion(
    suggestion_id: int,
    suggestion: SuggestionUpdate,
    suggestion_service: ISuggestionService = Depends(get_suggestion_service)
):
    return suggestion_service.update_suggestion(suggestion_id, suggestion)

@router.delete("/{suggestion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_suggestion(
    suggestion_id: int,
    suggestion_service: ISuggestionService = Depends(get_suggestion_service)
):
    suggestion_service.delete_suggestion(suggestion_id)

@router.post("/suggest", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def suggest(
    query: QueryRequest,
    suggestion_service: ISuggestionService = Depends(get_suggestion_service),
    history_service: IHistoryService = Depends(get_history_service)
):
    """
    Obtiene una sugerencia basada en la consulta del usuario.
    
    Utiliza búsqueda por similitud para encontrar la pregunta más cercana
    en la base de conocimiento y devuelve su respuesta.
    """
    # Obtener sugerencia
    response = suggestion_service.get_suggestion(query)
    
    # Guardar en historial
    history_service.save_query(
        query=query.query,
        suggestion=response.suggestion,
        score=response.similarity_score
    )
    
    return response