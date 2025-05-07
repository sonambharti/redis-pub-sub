import redis.asyncio as redis
from config import settings

async def redis_connect():
    try:
        redis_pool = redis.ConnectionPool.from_url(
            # settings.REDIS_URL,
            "redis://localhost:6379",
            # max_connections=settings.REDIS_MAX_CONNECTIONS,
            max_connections=5,
            decode_responses=True,
            encoding="utf-8"
        )
        redis_client = redis.Redis(connection_pool=redis_pool)
        print("Redis connection successful 🎉.")
        return redis_client
    except Exception as e:
        print(f"Redis connection failed: {e}")
        raise e
