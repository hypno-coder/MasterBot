from typing import Optional
from redis import Redis, asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from loader import config

database = AsyncIOMotorClient(config.db.db_host)
users_db = database.Master_DB.Master_Collection
settings_db = database.Master_DB.Master_State

redis_db = Redis(host="localhost", port=6379, db=0)

async def get_async_redis():
    async_redis = AsyncRedis()
    return await async_redis.get_client()

class AsyncRedis:
    _instance = None
    _redis_client = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    async def get_client(self) -> asyncio.Redis:
        if self._redis_client is None:
            await self.__initialize_redis()
        assert self._redis_client is not None, "Redis client не был инициализирован."
        return self._redis_client

    async def __initialize_redis(self):
        self._redis_client  = await asyncio.from_url("redis://localhost", db=1)
        print("Redis client initialized")

    async def close(self):
        if self._redis_client:
            await self._redis_client.close()
            print("Redis client closed")

