from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi import status
import redis
from core.config import settings


redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
MAX_REQUESTS = settings.RATE_LIMIT_MAX_REQUESTS
# MAX_REQUESTS = 100



class RateLimiterMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, request: Request, call_next):
        client_ip = request.client.host
        redis_key = f"{settings.RATE_LIMIT_REDIS_KEY_PREFIX}:{client_ip}"
        request_count = redis_client.get(redis_key)

        if not request_count:
            redis_client.set(redis_key, 0)
            request_count = 0

        if int(request_count) >= MAX_REQUESTS:
            return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={"message": "Too many requests"})

        redis_client.incr(redis_key)
        
        if settings.RATE_LIMIT_USE_TIME_FRAME:
            if redis_client.ttl(redis_key) == -1:
                redis_client.expire(redis_key, settings.RATE_LIMIT_TIME_WINDOW)
        
        response = call_next(request)
        return response
