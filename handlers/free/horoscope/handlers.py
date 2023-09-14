from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from config_data import SpamConfig
from keyboards import zodiac_menu
from lexicon import FreeMenuButtons 
from services import get_text_horoscope
from states import FSMHoroscope


horoscopeHandlerRouter: Router = Router()
flags: dict[str, str] = {'throrling_key': SpamConfig.horoscope_menu.name}

@horoscopeHandlerRouter.callback_query(F.data == FreeMenuButtons.Horoscope.name, flags=flags)
async def choose_zodiac(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message == None:
        return

    await callback.message.edit_text(text='Выбери свой знак зодиака!', reply_markup=zodiac_menu)
    await state.set_state(FSMHoroscope.get)


@horoscopeHandlerRouter.callback_query(FSMHoroscope.get, F.data != FreeMenuButtons.BackToFreeMenu.name)
async def get_horoscope(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.data == None or callback.message == None:
        return

    zodiac: str = callback.data
    text = await get_text_horoscope(zodiac=zodiac)
    if text == None:
        return

    await callback.message.edit_text(text=text, reply_markup=callback.message.reply_markup)


