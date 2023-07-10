from datetime import datetime, date
from .connector import database 
from states import UserStatus

date = datetime.now().date()

# user data querys
async def add_user(user, status: str = UserStatus.FREE.value):
    await database.insert_one({
                "_id": user.id,
                "username": user.username,
                "reg_date": str(date),
                "last_visit_date": str(date),
                "status": status
            })

async def get_user(user_id: int):
    return await database.find_one({"_id": user_id})

async def update_date_user(user_id, last_visit_date):
    if date > datetime.strptime(last_visit_date, "%Y-%m-%d").date():
        await database.update_one(
                {"_id": user_id}, 
                {"$set": {"last_visit_date": str(date)}})

async def get_total_users_count():
    return await database.estimated_document_count()

