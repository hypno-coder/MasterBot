from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import main_menu_keyboard 
from lexicon import BotText, BotBtnText
from config_data import SpamConfig

menuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.main_menu.name}

@menuRouter.message(CommandStart(), flags=flags)
async def start_main_menu(message: Message) -> None:
    await message.answer(text=BotText.main_menu,
                         reply_markup=main_menu_keyboard)
    await message.delete()

@menuRouter.message(Text(text=BotBtnText.CheckSub), flags=flags)
async def check_sub(message: Message) -> None:
    await message.answer(text=BotText.sub,
                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await message.answer(text=BotText.main_menu,
                         reply_markup=main_menu_keyboard)
    await message.delete()



