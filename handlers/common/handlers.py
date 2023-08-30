from aiogram import Router
from aiogram import Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from lexicon import BotText
from config_data import SpamConfig  

handlersRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.common.name}

@handlersRouter.message(Command(commands='delmenu'), flags=flags)
async def remove_command_menu(message: Message, bot: Bot):
    await bot.delete_my_commands()
    await message.answer(text=BotText.remove_command_menu)

@handlersRouter.message(Command(commands='cancel'), flags=flags)
async def cancel_state(message: Message, state: FSMContext):
    await message.answer(text=BotText.cancel_state)
    await state.clear()

@handlersRouter.message(Command(commands='help'), flags=flags)
async def help(message: Message):
    await message.answer(text=BotText.help)

