from redis import Redis, asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from loader import config

database = AsyncIOMotorClient(config.db.db_host)
users_db = database.Master_DB.Master_Collection
settings_db = database.Master_DB.Master_State

redis_db = Redis(host="localhost", port=6379, db=0)

async def get_async_redis() -> asyncio.Redis:
    return await asyncio.from_url("redis://localhost", db=1)

