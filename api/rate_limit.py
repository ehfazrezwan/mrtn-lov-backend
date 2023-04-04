from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi import status
import redis


redis_client = redis.Redis(host='redis', port=6379, db=0)
MAX_REQUESTS = 10


class RateLimiterMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, request: Request, call_next):
        client_ip = request.client.host
        redis_key = f"rate_limit:{client_ip}"
        request_count = redis_client.get(redis_key)

        if not request_count:
            redis_client.set(redis_key, 0)
            request_count = 0

        if int(request_count) >= MAX_REQUESTS:
            return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={"message": "Too many requests"})

        redis_client.incr(redis_key)
        response = await call_next(request)
        return response
