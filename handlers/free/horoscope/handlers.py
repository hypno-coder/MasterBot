from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config_data import SpamConfig
from keyboards import (action_zodiac_compare_menu, active_zodiac_menu,
                       gender_compare_menu, get_zodiac_compare_menu,
                       zodiac_menu)
from lexicon import (ActionChooseGenderButtons, CompareZodiacButtons,
                     FreeMenuButtons, GetCompareZodiacButtons,
                     HoroscopeLexicon, PeriodZodiacButtons,
                     UnitedZodiacButtons, ZodiacButtons, horoscopeStars)
from services import ComparisonType, Horoscope
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
    FSMHoroscope.get,
    lambda a: a.data in UnitedZodiacButtons.__members__
    and a.data != UnitedZodiacButtons.Compare.name,
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

    horoscope: Horoscope = Horoscope(
        zodiac=ZodiacButtons[data["zodiac"]], period=PeriodZodiacButtons[period]
    )
    resp = await horoscope.get_horo()
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


@horoscopeHandlerRouter.callback_query(
    lambda a: a.data == CompareZodiacButtons.Compare.name
)
async def choose_you_gender(callback: CallbackQuery, state: FSMContext) -> None:
    message_text = "Укажите свой пол"
    assert callback.message
    await callback.message.edit_text(
        text=message_text, reply_markup=gender_compare_menu
    )
    await state.set_state(FSMHoroscope.choose_your_zodiac)


@horoscopeHandlerRouter.callback_query(
    FSMHoroscope.choose_your_zodiac,
    lambda a: a.data in ActionChooseGenderButtons.__members__,
)
async def choose_your_zodiac(callback: CallbackQuery, state: FSMContext) -> None:
    assert callback.data
    assert callback.message
    gender_partner = (
        ActionChooseGenderButtons.Male.name
        if callback.data == ActionChooseGenderButtons.Female.name
        else ActionChooseGenderButtons.Female.name
    )
    await state.set_data(
        {"your_gender": callback.data, "gender_partner": gender_partner}
    )

    message_text = f"Вы: {ActionChooseGenderButtons[callback.data].value}\nПартнер: {ActionChooseGenderButtons[gender_partner].value} \n\n Укажите Ваш знак зодиака"
    await callback.message.edit_text(text=message_text, reply_markup=zodiac_menu)
    await state.set_state(FSMHoroscope.choose_partner_zodiac)


@horoscopeHandlerRouter.callback_query(
    FSMHoroscope.choose_partner_zodiac, lambda a: a.data in ZodiacButtons.__members__
)
async def choose_partner_zodiac(callback: CallbackQuery, state: FSMContext) -> None:
    assert callback.data
    assert callback.message
    data = await state.get_data()
    data.update({"your_zodiac": callback.data})

    your_gender = ActionChooseGenderButtons[data["your_gender"]].value
    your_zodiac = ZodiacButtons[callback.data].value
    gender_partner = ActionChooseGenderButtons[data["gender_partner"]].value

    message_text = f"Вы: {your_gender}, {your_zodiac}\nПартнер: {gender_partner}\n\n Укажите знак зодиака Вашего партнера"
    await state.update_data(data)
    await callback.message.edit_text(text=message_text, reply_markup=zodiac_menu)
    await state.set_state(FSMHoroscope.get_compare_zodiac)


@horoscopeHandlerRouter.callback_query(
    FSMHoroscope.get_compare_zodiac, lambda a: a.data in ZodiacButtons.__members__
)
async def get_compare_zodiac(callback: CallbackQuery, state: FSMContext) -> None:
    assert callback.data
    assert callback.message
    data = await state.get_data()

    your_gender = ActionChooseGenderButtons[data["your_gender"]].value
    your_zodiac = ZodiacButtons[data["your_zodiac"]].value
    gender_partner = ActionChooseGenderButtons[data["gender_partner"]].value
    partner_zodiac = ZodiacButtons[callback.data].value

    message_text = (
        f"===================\nВы: {your_gender}, {your_zodiac}\nПартнер: {gender_partner}, {partner_zodiac}\n==================="
    )
    data.update(
        {
            ActionChooseGenderButtons[data["your_gender"]]
            .name: ZodiacButtons[data["your_zodiac"]]
            .name,
            ActionChooseGenderButtons[data["gender_partner"]].name: callback.data,
        }
    )
    await state.update_data(data)
    await callback.message.edit_text(text=message_text)
    await state.set_state(FSMHoroscope.choose_partner_zodiac)
    await callback.message.edit_text(
        text=message_text, reply_markup=get_zodiac_compare_menu
    )
    await state.set_state(FSMHoroscope.compare_response)


@horoscopeHandlerRouter.callback_query(
    FSMHoroscope.compare_response,
    lambda a: a.data in GetCompareZodiacButtons.__members__,
)
async def compare_response(callback: CallbackQuery, state: FSMContext) -> None:

    data = await state.get_data()
    horoscope: Horoscope = Horoscope(
        comparison=ComparisonType(
            Female=ZodiacButtons[data["Female"]], Male=ZodiacButtons[data["Male"]]
        )
    )
    result = await horoscope.get_compare()
    assert callback.message
    message_text = f"{result['title']}\n\n{result['text']}"
    await callback.message.edit_text(
        text=message_text, reply_markup=action_zodiac_compare_menu
    )
