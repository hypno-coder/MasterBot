from datetime import datetime, date
from .connector import database 

date = datetime.now().date()

# user data querys
async def add_user(user) -> None:
    await database.insert_one({
                "_id": user.id,
                "username": user.username,
                "reg_date": str(date),
                "last_visit_date": str(date),
            })

async def update_date_user(user_id) -> None:
    pass

