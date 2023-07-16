from aiogram import Router
from aiogram import Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from lexicon import BotText
from config_data import SpamConfig  

handlersRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.common.name}

@handlersRouter.message(Command(commands='delmenu'), flags=flags)
async def remove_command_menu(message: Message, bot: Bot):
    await bot.delete_my_commands()
    await message.answer(text=BotText.remove_command_menu)

@handlersRouter.message(Command(commands='cancel'), ~StateFilter(default_state))
async def cancel_state(message: Message, state: FSMContext):
    await message.answer(text=BotText.cancel_state)
    await state.clear()
