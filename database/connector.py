from motor.motor_asyncio import AsyncIOMotorClient 
import redis
from loader import config


database = AsyncIOMotorClient(config.db.db_host)
users_db = database.Master_DB.Master_Collection
settings_db = database.Master_DB.Master_State

redis_db = redis.Redis(host='localhost', port=6379, db=0)

