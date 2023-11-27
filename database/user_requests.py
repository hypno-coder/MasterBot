from datetime import datetime
from database.connector import users_db 
from errors import send_error_message
from lexicon import QueryErrText
from states import UserStatus


class User:
    now = datetime.now().date()

    def __init__(self, user, status: str = UserStatus.FREE.value):
        self.user_id: int = user.id
        self.username: str = user.username
        self.reg_date: str
        self.last_visit_date: str
        self.status: str = status

    @staticmethod
    async def get(user_id):
        result = await users_db.find_one({'_id': user_id})
        return result

    @staticmethod
    async def get_all() -> list:
        cursor = users_db.find()
        result = await cursor.to_list(length=None)
        return result

    @staticmethod
    async def update(user_id, field, data):
        try:
            await users_db.update_one(
                    {'_id': user_id}, 
                    {'$set': {field: data}})
        except Exception:
            await send_error_message(QueryErrText.UPDATE_USER.value)
            raise Exception(QueryErrText.UPDATE_USER.value)

    async def add(self):
        data = {
                '_id': self.user_id,
                'username': self.username,
                'reg_date': str(self.now),
                'last_visit_date': str(self.now),
                'status': self.status,
                'fio': None,
                'birthday': None,
                'purchases': [],
             }
        try:
            await users_db.insert_one(data)
        except Exception:
            await send_error_message(QueryErrText.INSERT_USER.value)
        finally:
            return data

    async def get_or_create(self):
        try:
            result = await self.get(self.user_id)
            if result != None:
                self.reg_date = result['reg_date']
                self.last_visit_date = result['last_visit_date']
                is_user = 'get'
                return result, is_user
            result = await self.add()
            is_user = 'create'
            return result, is_user
        except Exception:
            await send_error_message('Упал метод get_or_create')
            raise Exception('Упал метод get_or_create')

    async def date_update(self):
        try:
            if self.now > datetime.strptime(self.last_visit_date, '%Y-%m-%d').date():
                await users_db.update_one(
                        {'_id': self.user_id}, 
                        {'$set': {'last_visit_date': str(self.now)}})
        except Exception:
            await send_error_message(QueryErrText.UPDATE_USER.value)
            raise Exception(QueryErrText.UPDATE_USER.value)

    async def total_count(self):
        try:
            return await users_db.estimated_document_count()
        except Exception:
            await send_error_message(QueryErrText.USERS_COUNT.value)
