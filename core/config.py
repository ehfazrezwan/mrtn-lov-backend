from typing import Any, Dict, List, Optional, Union
from pydantic import BaseSettings, AnyHttpUrl, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = ""
    PROJECT_NAME: str = "FastAPI Starter"
    PROJECT_DESCRIPTION: str = "A starter template for FastAPI"
    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_POOL_SIZE: int = 5
    SQLALCHEMY_MAX_OVERFLOW: int = 10
    RATE_LIMIT_DEFAULT: int = 500
    RATE_LIMIT_WINDOW: int = 60
    RATE_LIMIT_LIMITER: str = "flask_limiter.Limiter"
    
    @validator("SQLALCHEMY_DATABASE_URI")
    def check_database_url(cls, v: str) -> str:
        if not v.startswith("postgresql"):
            raise ValueError("Only PostgreSQL databases are supported")
        return v
    
    class Config:
        case_sensitive = True


settings = Settings()
