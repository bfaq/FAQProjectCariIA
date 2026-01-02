from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
from app.api.exception_handlers import register_exception_handlers

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API REST con FastAPI - Arquitectura en capas"
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
register_exception_handlers(app)


@app.get("/")
def root():
    return {"message": "FastAPI corriendo en Docker", "version": settings.VERSION}

