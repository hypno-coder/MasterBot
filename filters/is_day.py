from datetime import datetime
from aiogram.types import Message 
from aiogram.filters import BaseFilter

class DayFilter(BaseFilter):
    key: str = 'is_day'
    thursday: int = 4
    
    def __init__(self, is_day):
        self.is_day = is_day

    async def __call__(self, message: Message):
        today = datetime.today()
        return today.weekday() == self.thursday
