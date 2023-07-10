from datetime import datetime, date
from .connector import users_db 
from errors import send_error_message
from lexicon import QueryErrText
from states import UserStatus


class User:
    now = datetime.now().date()

    def __init__(self, user, status: str = UserStatus.FREE.value):
        self.user_id: int = user.id
        self.username: str = user.username
        self.reg_date: str = str(self.now)
        self.last_visit_date: str = str(self.now)
        self.status: str = status

    @staticmethod
    async def get(user_id):
        try:
            return await users_db.find_one({"_id": user_id})
        except Exception:
            await send_error_message(QueryErrText.FIND_USER.value)

    @staticmethod
    async def update(user_id, field, data):
        try:
            await users_db.update_one(
                    {"_id": user_id}, 
                    {"$set": {field: data}})
        except Exception:
            await send_error_message(QueryErrText.UPDATE_USER.value)

    async def add(self):
        try:
            await users_db.insert_one({
                        "_id": self.user_id,
                        "username": self.username,
                        "reg_date": self.reg_date,
                        "last_visit_date": self.last_visit_date,
                        "status": self.status
                    })
            return True
        except Exception:
            await send_error_message(QueryErrText.INSERT_USER.value)
            return False
    
    async def check(self):
        try:
            result = await users_db.find_one({"_id": self.user_id})
            if result == None:
                return False
            return True
        except Exception:
            await send_error_message(QueryErrText.FIND_USER.value)

    async def date_update(self):
        try:
            if self.now > datetime.strptime(self.last_visit_date, "%Y-%m-%d").date():
                await users_db.update_one(
                        {"_id": self.user_id}, 
                        {"$set": {"last_visit_date": str(self.now)}})
        except Exception:
            await send_error_message(QueryErrText.UPDATE_USER.value)

    async def total_count(self):
        try:
            return await users_db.estimated_document_count()
        except Exception:
            await send_error_message(QueryErrText.USERS_COUNT.value)
