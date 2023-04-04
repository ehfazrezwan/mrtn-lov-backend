import unittest
import redis
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import status
from unittest.mock import MagicMock, AsyncMock, patch
from core.config import settings
from api.rate_limit import RateLimiterMiddleware


class TestRateLimiterMiddleware(unittest.IsolatedAsyncioTestCase):

    async def setUp(self):
        self.app = FastAPI()
        self.redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        self.middleware = RateLimiterMiddleware(self.app)

    # async def tearDown(self):
    #     await self.redis_client.flushdb()
    
    async def test_no_request_count_in_redis(self):
        request = Request({"type": "http", "client": ("127.0.0.1", 80)})
        call_next = MagicMock(return_value=JSONResponse(content={"message":"Hello, world!"}))
        response = await self.middleware(request, call_next)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body, b'{"message":"Hello, world!"}')
        self.assertEqual(self.redis_client.get("rate_limit:127.0.0.1"), b'1')

    async def test_max_requests_reached(self):
        request = Request({"type": "http", "client": ("127.0.0.1", 80)})
        self.redis_client.set("rate_limit:127.0.0.1", settings.RATE_LIMIT_MAX_REQUESTS)
        call_next = MagicMock(return_value=JSONResponse(content={"message": "Hello, world!"}))
        response = await self.middleware(request, call_next)

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(response.body, b'{"message":"Too many requests"}')

    async def test_request_count_below_max(self):
        request = Request({"type": "http", "client": ("127.0.0.1", 80)})
        self.redis_client.set("rate_limit:127.0.0.1", settings.RATE_LIMIT_MAX_REQUESTS - 1)
        call_next = MagicMock(return_value=JSONResponse(content={"message": "Hello, world!"}))
        response = await self.middleware(request, call_next)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body, b'{"message":"Hello, world!"}')
        self.assertEqual(self.redis_client.get("rate_limit:127.0.0.1"), b'10')

    async def test_use_time_frame_true(self):
        request = Request({"type": "http", "client": ("127.0.0.1", 80)})
        with patch.object(self.redis_client, "ttl", return_value=-1):
            with patch.object(self.redis_client, "expire", return_value=None):
                with patch.object(settings, "RATE_LIMIT_USE_TIME_FRAME", return_value=True):
                    call_next = MagicMock(return_value=JSONResponse(content={"message":"Hello, world!"}))
                    response = await self.middleware(request, call_next)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.body, b'{"message":"Hello, world!"}')
        self.assertEqual(self.redis_client.ttl("rate_limit:127.0.0.1"), settings.RATE_LIMIT_TIME_WINDOW)
