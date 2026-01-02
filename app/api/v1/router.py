from fastapi import APIRouter
from app.api.v1.endpoints import suggestions, history

api_router = APIRouter()
api_router.include_router(suggestions.router, prefix="/suggestions", tags=["suggestions"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
