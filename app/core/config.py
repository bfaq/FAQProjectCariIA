from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FAQ Project"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    class ConfigDict:
        case_sensitive = True

settings = Settings()