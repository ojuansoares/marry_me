from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    FRONTEND_URL: str = "http://localhost:3000"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Casamento API"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 