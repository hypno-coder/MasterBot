from datetime import datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message


class AgeFilter(BaseFilter):
    key: str = "is_age"
    start_age: int = 13
    end_age: int = 80

    def __init__(self, is_age):
        self.is_age = is_age

    async def __call__(self, message: Message):
        if message.text == None:
            return False
        try:
            birthdate = datetime.strptime(message.text, "%d.%m.%Y")
        except ValueError:
            return False

        current_date = datetime.now()
        age = current_date.year - birthdate.year

        if age > self.start_age and age < self.end_age:
            return True
        else:
            return False
