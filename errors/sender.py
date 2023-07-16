from loader import bot, config

async def send_error_message(error_text) -> None:
    await bot.send_message(
            chat_id=config.tg_bot.chat_log, 
            text=error_text) 

