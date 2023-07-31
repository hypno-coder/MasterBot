# import re
from typing import cast
from datetime import datetime
from aiogram.types import Message 
from aiogram.filters import BaseFilter

class DateFilter(BaseFilter):
    key: str = 'is_date'
    thursday: int = 3
    
    def __init__(self, is_date):
        self.is_date = is_date

    async def __call__(self, message: Message):
        if message.text == None or self.is_day_today():
            return False

        try:
            datetime.strptime(message.text, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    def is_day_today(self):
        today = datetime.today()
        return today.weekday() == self.thursday

