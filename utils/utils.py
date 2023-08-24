import random
from asyncio import sleep 
from aiogram.types.input_file import FSInputFile

from loader import bot
from lexicon import BotText

async def remove_message(chat_id: int, message_id: int, delay: int = 60) -> None:
    try:
        await sleep(delay)
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as ex:
        print(f'{BotText.remove_message_error} \n {ex}')

async def send_message_with_delay(
        chat_id: int, 
        min_delay: int = 1800, 
        max_delay: int = 4800,
        text: str | None = None,
        video: FSInputFile | None = None,
        document:  FSInputFile | None = None,
        document_caption: str = ''
        ) -> None:

    await bot.send_message(
            chat_id,
            text=BotText.message_delay + f'{round(min_delay/60)}-{round(max_delay/60)} минут')

    delay = random.randint(min_delay, max_delay)
    await sleep(delay)
    if text != None:
        await bot.send_message(chat_id, text)
    if video != None:
        await bot.send_video(chat_id, video)
    if document != None:
        await bot.send_document(chat_id, document, caption=document_caption)
