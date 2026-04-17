from datetime import datetime
from aiogram.types import Message
from aiogram.filters import BaseFilter

from loader import config

class DayFilter(BaseFilter):
    key: str = 'is_day'
    thursday: int = 3
    def __init__(self, is_day):
        self.is_day = is_day

    async def __call__(self, event: Message):
        assert event.from_user
        if event.message.chat.id in config.tg_bot.admin_ids:
            return True
        else:
            today = datetime.today()
            return today.weekday() == self.thursday
