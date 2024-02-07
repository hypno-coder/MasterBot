from loader import bot, config
from aiogram.types import Message 

async def send_error_message(error_text) -> Message:
    result = await bot.send_message(
            chat_id=config.tg_bot.chat_log, 
            text=error_text) 
    return result

