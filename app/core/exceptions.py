class DomainError(Exception):
    def __init__(self, message: str | None = None):
        self.message = message or "Error de dominio"
        super().__init__(self.message)


class NotFoundError(DomainError):
    pass


class AlreadyExistsError(DomainError):
    pass


class ValidationError(DomainError):
    pass


class ServiceUnavailableError(DomainError):
    pass