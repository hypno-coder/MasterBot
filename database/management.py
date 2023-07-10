from datetime import datetime, date
from .connector import database 
from errors import send_error_message
from lexicon import QueryErrText
from states import UserStatus

date = datetime.now().date()

# user data querys
async def add_user(user, status: str = UserStatus.FREE.value):
    try:
        await database.insert_one({
                    "_id": user.id,
                    "username": user.username,
                    "reg_date": str(date),
                    "last_visit_date": str(date),
                    "status": status
                })
        return True
    except Exception:
        await send_error_message(QueryErrText.INSERT_USER.value)
        return False


async def get_user(user_id: int):
    try:
        return await database.find_one({"_id": user_id})
    except Exception:
        await send_error_message(QueryErrText.FIND_USER.value)

async def update_date_user(user_id, last_visit_date):
    try:
        if date > datetime.strptime(last_visit_date, "%Y-%m-%d").date():
            await database.update_one(
                    {"_id": user_id}, 
                    {"$set": {"last_visit_date": str(date)}})
    except Exception:
        await send_error_message(QueryErrText.UPDATE_USER.value)


async def get_total_users_count():
    try:
        return await database.estimated_document_count()
    except Exception:
        await send_error_message(QueryErrText.USERS_COUNT.value)

