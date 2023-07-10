from motor.motor_asyncio import AsyncIOMotorClient 
from loader import config


database = AsyncIOMotorClient(config.db.db_host)
users_db = database.Master_DB.Master_Collection
settings_db = database.Master_DB.Master_State


