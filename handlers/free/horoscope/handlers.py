from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from config_data import SpamConfig
from keyboards import zodiac_menu
from lexicon import FreeMenuButtons, HoroscopeLexicon, ZodiacButtons 
from services import Horoscope 
from states import FSMHoroscope

horoscopeHandlerRouter: Router = Router()
flags: dict[str, str] = {'throrling_key': SpamConfig.horoscope_menu.name}


@horoscopeHandlerRouter.callback_query(F.data == FreeMenuButtons.Horoscope.name, flags=flags)
async def choose_zodiac(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message == None:
        return

    await callback.message.edit_text(text=HoroscopeLexicon.make_choise, reply_markup=zodiac_menu)
    await state.set_state(FSMHoroscope.get)


@horoscopeHandlerRouter.callback_query(FSMHoroscope.get, lambda a: a.data in ZodiacButtons.__members__)
async def get_horoscope(callback: CallbackQuery) -> None:
    await callback.answer()
    if not callback.data or not callback.message:
        return
    zodiac: str = callback.data
    horoscope: Horoscope = Horoscope(zodiac)
    resp: str | None = await horoscope.get()
    try:
        if not resp:
            await callback.message.edit_text(
                text=HoroscopeLexicon.error, reply_markup=callback.message.reply_markup)
            return
        name = getattr(ZodiacButtons, zodiac).value
        result: str = f'<b>{name}: </b> \n\n {resp}'
        await callback.message.edit_text(text=result, reply_markup=callback.message.reply_markup)

    except TelegramBadRequest:
        await callback.answer()
