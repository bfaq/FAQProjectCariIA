from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    DomainError,
    NotFoundError,
    AlreadyExistsError,
    ServiceUnavailableError
)
import logging

logger = logging.getLogger(__name__)

def register_exception_handlers(app):

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception", exc_info=exc)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Ocurrió un error interno, por favor intenta de nuevo más tarde o comunicate con un administrador."
            }
        )

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message}
        )

    @app.exception_handler(AlreadyExistsError)
    async def already_exists_handler(request: Request, exc: AlreadyExistsError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message}
        )

    @app.exception_handler(ServiceUnavailableError)
    async def service_unavailable_handler(request: Request, exc: ServiceUnavailableError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": exc.message}
        )

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )
