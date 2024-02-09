import redis

from database.connector import redis_db
from errors import send_error_message
from lexicon import LockControllerLexicon


class BotAccessController:
    BOT_LOCK_KEY = "bot:lock"

    async def lock(self):
        try:
            result = redis_db.set(self.BOT_LOCK_KEY, "locked")
            if result != None:
                return result
        except redis.RedisError as e:
            await self.__handle_redis_error(LockControllerLexicon.blocking_err, e)

    async def unlock(self):
        try:
            result = redis_db.set(self.BOT_LOCK_KEY, "unlocked")
            if result != None:
                return result
        except redis.RedisError as e:
            await self.__handle_redis_error(LockControllerLexicon.unblocking_err, e)

    async def is_locked(self):
        try:
            return redis_db.get(self.BOT_LOCK_KEY) == b"locked"
        except redis.RedisError as e:
            await self.__handle_redis_error(LockControllerLexicon.check_status_err, e)

    async def __handle_redis_error(self, message, exception):
        await send_error_message(message)
        print(exception)
