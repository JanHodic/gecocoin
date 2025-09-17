from __future__ import annotations
import asyncio
from typing import Optional


try:
    from redis.asyncio import Redis
except Exception: # redis optional fallback
        Redis = None # type: ignore


from .settings import REDIS_URL


redis: Optional[Redis] = None


async def get_redis() -> Optional[Redis]:
    global redis
    if redis is None and Redis is not None:
        redis = Redis.from_url(REDIS_URL, decode_responses=True)
    return redis


async def cache_get(key: str) -> Optional[str]:
    r = await get_redis()
    if not r:
        return None
    try:
        return await r.get(key)
    except Exception:
        return None


async def cache_setex(key: str, ttl: int, value: str) -> None:
    r = await get_redis()
    if not r:
        return
    try:
        await r.setex(key, ttl, value)
    except Exception:
        pass