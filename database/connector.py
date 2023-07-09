from motor.motor_asyncio import AsyncIOMotorClient 
from loader import config


cluster = AsyncIOMotorClient(config.db.db_host)
database = cluster.Master_DB.Master_Collection


