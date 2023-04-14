from fastapi import FastAPI

# from .rate_limit import RateLimiterMiddleware
from .prompt import router as prompt_router, discord_client, start_discord_client

app = FastAPI()


@app.on_event("startup")
async def app_startup():
    await start_discord_client()


# app.add_middleware(RateLimiterMiddleware)
@app.on_event("shutdown")
async def app_shutdown():
    await discord_client.close()


app.include_router(prompt_router)
