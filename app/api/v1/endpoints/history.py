from typing import List
from fastapi import APIRouter, Depends, status
from app.schemas.schemas import HistoryResponse
from app.services.history_service import IHistoryService
from app.api.dependencies import get_history_service

router = APIRouter()

@router.get("/", response_model=List[HistoryResponse])
async def get_history(
    history_service: IHistoryService = Depends(get_history_service)
):
    """
    Devuelve el historial completo de consultas y sugerencias.
    
    Las consultas se devuelven ordenadas por fecha (más reciente primero).
    """
    history = history_service.get_history()
    return [
        HistoryResponse(
            query=h.query,
            suggestion=h.suggestion,
            similarity_score=round(h.similarity_score, 2),
            timestamp=h.created_at
        )
        for h in history
    ]
