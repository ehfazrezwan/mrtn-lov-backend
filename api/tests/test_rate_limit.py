import asyncio
import unittest
import redis
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi import status
from api.rate_limit import RateLimiterMiddleware

class TestRateLimiterMiddleware(unittest.TestCase):
    
    def setUp(self):
        self.app = FastAPI()

    async def test_middleware_with_valid_request(self):
        middleware = RateLimiterMiddleware(self.app)
        request = Request({"type": "http", "client": {"host": "127.0.0.1"}})
        async def call_next(req):
            return JSONResponse(content={"message": "OK"})
        response = await middleware(request, call_next)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    async def test_middleware_with_too_many_requests(self):
        middleware = RateLimiterMiddleware(self.app)
        async with redis.Redis(host='redis', port=6379, db=1) as redis_client:
            redis_client.flushdb()
            redis_client.set("rate_limit:127.0.0.1", 10)
            request = Request({"type": "http", "client": {"host": "127.0.0.1"}})
            async def call_next(req):
                return JSONResponse(content={"message": "OK"})
            response = await middleware(request, call_next)
            self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
            self.assertEqual(response.json(), {"message": "Too many requests"})

    async def tearDown(self):
        async with redis.Redis(host='redis', port=6379, db=1) as redis_client:
            await redis_client.flushdb()

if __name__ == '__main__':
    asyncio.run(unittest.main()) 


