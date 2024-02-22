from datetime import datetime
from aiogram.types import Message 
from aiogram.filters import BaseFilter

class DateFilter(BaseFilter):
    key: str = 'is_date'
    
    def __init__(self, is_date):
        self.is_date = is_date
    async def __call__(self, message: Message):
        if message.text == None:
            return False

        try:
            datetime.strptime(message.text, "%d.%m.%Y")
            return True
        except Exception:
            return False
