from fastapi import FastAPI

from core.config import settings
from .prompt import router as prompt_router


app = FastAPI()


app.include_router(prompt_router)
