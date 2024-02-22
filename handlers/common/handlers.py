from asyncio import create_task

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config_data import SpamConfig
from lexicon import CommonLexicon
from utils import remove_message

handlersRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.common.name}


@handlersRouter.message(Command(commands="deletecommandmenu"), flags=flags)
async def remove_command_menu(message: Message, bot: Bot):
    await bot.delete_my_commands()
    await message.answer(text=CommonLexicon.remove_command_menu)


@handlersRouter.message(Command(commands="cancel"), flags=flags)
async def cancel_state(message: Message, state: FSMContext):
    await state.clear()
    chat_id = message.chat.id
    message_id = message.message_id
    data = await message.answer(text=CommonLexicon.cancel_state)

    create_task(
        remove_message(chat_id=data.chat.id, message_id=data.message_id, delay=2)
    )
    create_task(remove_message(chat_id=chat_id, message_id=message_id, delay=3))


@handlersRouter.message(Command(commands="help"), flags=flags)
async def help(message: Message):
    await message.answer(text=CommonLexicon.help)
