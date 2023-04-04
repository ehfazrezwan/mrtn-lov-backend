from fastapi import FastAPI
from .rate_limit import RateLimiterMiddleware
from .prompt import router as prompt_router

app = FastAPI()
app.add_middleware(RateLimiterMiddleware)

app.include_router(prompt_router)
