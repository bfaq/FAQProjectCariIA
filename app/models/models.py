from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Suggestion:
    id: int
    question: str
    suggestion: str
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class QueryHistory:
    id: int
    query: str
    suggestion: str
    similarity_score: float
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()