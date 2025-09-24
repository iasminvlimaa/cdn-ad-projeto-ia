from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Ambas as variáveis agora são opcionais
    DATABASE_URL: Optional[str] = None
    EXTERNAL_DB_URL: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()