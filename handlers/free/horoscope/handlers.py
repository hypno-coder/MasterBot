from aiogram import Router
from aiogram.types import CallbackQuery

from config_data import SpamConfig
from keyboards import zodiac_menu
from lexicon import FreeMenuButtons 

horoscopeHandlerRouter: Router = Router()
flags: dict[str, str] = {'throrling_key': SpamConfig.horoscope_menu.name}

@horoscopeHandlerRouter.callback_query(
        lambda a: a.data == FreeMenuButtons.Horoscope.name, flags=flags)
async def choose_zodiac(callback: CallbackQuery) -> None:
    if callback.message == None:
        return

    await callback.message.edit_text(text='Выбери свой знак зодиака!', reply_markup=zodiac_menu)

