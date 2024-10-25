from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config_data import SpamConfig
from keyboards import active_zodiac_menu, zodiac_menu
from lexicon import (FreeMenuButtons, HoroscopeLexicon, PeriodZodiacButtons,
                     UnitedZodiacButtons, ZodiacButtons, horoscopeStars)
from services import Horoscope
from states import FSMHoroscope

horoscopeHandlerRouter: Router = Router()
flags: dict[str, str] = {"throrling_key": SpamConfig.horoscope_menu.name}


@horoscopeHandlerRouter.callback_query(
    F.data == FreeMenuButtons.Horoscope.name, flags=flags
)
async def choose_zodiac(callback: CallbackQuery, state: FSMContext) -> None:
    assert callback.message
    await callback.message.edit_text(
        text=HoroscopeLexicon.make_choise, reply_markup=zodiac_menu
    )
    await state.set_state(FSMHoroscope.get)


@horoscopeHandlerRouter.callback_query(
    FSMHoroscope.get, lambda a: a.data in UnitedZodiacButtons.__members__
)
async def get_horoscope(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    if not callback.data or not callback.message:
        return
    period = "today"
    value: str = callback.data

    if value in ZodiacButtons.__members__:
        await state.set_data({"zodiac": value})
    if value in PeriodZodiacButtons.__members__:
        period = value
    data = await state.get_data()

    horoscope: Horoscope = Horoscope(zodiac=data["zodiac"], period=period)
    resp = await horoscope.get()
    finance = horoscopeStars[resp["finance"]]
    health = horoscopeStars[resp["health"]]
    love = horoscopeStars[resp["love"]]
    try:
        if not resp:
            await callback.message.edit_text(
                text=HoroscopeLexicon.error, reply_markup=callback.message.reply_markup
            )
            return
        result: str = (
            f"<b>{resp['title']}: </b> \n\n {resp['text']} \n\n <b>{resp['title']}</b>\n\n <b>Финансы</b>   {finance}\n <b>Здоровье</b>  {health}\n <b>Любовь</b>     {love}"
        )
        await callback.message.edit_text(text=result, reply_markup=active_zodiac_menu)

    except TelegramBadRequest:
        await callback.answer()
