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

    # For rate limiting
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    RATE_LIMIT_MAX_REQUESTS: int
    RATE_LIMIT_TIME_WINDOW: int
    RATE_LIMIT_REDIS_KEY_PREFIX: str

    RATE_LIMIT_USE_TIME_FRAME: bool = False

    BANANA_API_KEY: str = "3a79eef5-7ec7-40ef-be8f-be757e58f6e0"
    BANANA_MODEL_KEY: str = "9edbdd67-2078-4eff-935f-6a0b62c869f3"

    DISCORD_BOT_TOKEN: str = (
        "MTA5NjEzMjI3NzAzNTA4MTg4OQ.Gt-8HU.kNWQ-itfCvx0CGOMIgM4wqUrdye03GAMdvVSI4"
    )
    DISCORD_IMG_CHANNEL_ID: int = 1096149128305717248
    DISCORD_ERROR_CHANNEL_ID: int = 1096230892529258578

    DISCORD_TEST_CHANNEL_ID: int = 1096466127233761371

    @validator("SQLALCHEMY_DATABASE_URI")
    def check_database_url(cls, v: str) -> str:
        if not v.startswith("postgresql"):
            raise ValueError("Only PostgreSQL databases are supported")
        return v

    class Config:
        case_sensitive = True


settings = Settings()
