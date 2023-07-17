# import re
from datetime import datetime
from aiogram import types
from aiogram.filters import BaseFilter

class DateFilter(BaseFilter):
    key = 'is_date'
    
    def __init__(self, is_date):
        self.is_date = is_date

    async def __call__(self, message: types.Message):
        if message.text == None:
            return
        # date_pattern = r'\d{2}\.\d{2}\.\d{4}'
        # return bool(re.match(date_pattern, message.text))
        try:
            datetime.strptime(message.text, "%d.%m.%Y")
            return True
        except ValueError:
            return False

