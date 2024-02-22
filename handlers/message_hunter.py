from asyncio import create_task

from aiogram import Router
from aiogram.types import Message

from config_data import SpamConfig
from lexicon import CommonLexicon
from utils import remove_message

messageHunterRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.common.name}


@messageHunterRouter.message()
async def message_hunter(message: Message):
    chat_id = message.chat.id
    message_id = message.message_id
    data = await message.answer(text=CommonLexicon.help_message)

    create_task(remove_message(chat_id=chat_id, message_id=message_id, delay=1))
    create_task(
        remove_message(chat_id=data.chat.id, message_id=data.message_id, delay=10)
    )
