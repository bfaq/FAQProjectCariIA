from pydantic import BaseModel, Field, constr
from datetime import datetime
from typing import Optional, Annotated

class SuggestionBase(BaseModel):
    question: str = Field(..., min_length=3, description="Pregunta")
    suggestion: str = Field(..., min_length=3, description="Respuesta a la pregunta")

class SuggestionCreate(SuggestionBase):
    pass

class SuggestionUpdate(SuggestionBase):
    question: Optional[Annotated[str, Field(min_length=3)]] = None
    suggestion: Optional[Annotated[str, Field(min_length=3)]] = None

class SuggestionResponse(SuggestionBase):
    id: int
    created_at: datetime
    
    class ConfigDict:
        from_attributes = True

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500, description="Consulta del usuario")
    
    class ConfigDict:
        json_schema_extra = {
            "example": {
                "query": "¿Cómo cambio mi contraseña?"
            }
        }

class QueryResponse(BaseModel):
    suggestion: str = Field(..., description="Sugerencia basada en la consulta")
    similarity_score: float = Field(..., description="Puntuación de similitud (0-1)")
    matched_question: Optional[str] = Field(None, description="Pregunta que coincidió")
    
    class ConfigDict:
        json_schema_extra = {
            "example": {
                "suggestion": "Puedes cambiar tu contraseña en la sección de configuración de tu perfil.",
                "similarity_score": 0.95,
                "matched_question": "¿Cómo cambio mi contraseña?"
            }
        }

class HistoryResponse(BaseModel):
    query: str
    suggestion: str
    similarity_score: float
    timestamp: datetime
    
    class ConfigDict:
        from_attributes = True
