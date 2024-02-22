import random
from decimal import Decimal
from typing import cast

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from config_data import SpamConfig
from filters import AgeFilter, DateFilter
from keyboards import (calendar_action_menu_keyboard,
                       get_data_by_month_for_a_calendar, get_payment_keyboard)
from lexicon import (CalendarActionMenuButtons, CalendarLexicon,
                     CalendarMenuButtons, CalendarSelectMonthMenuButtons,
                     CommonLexicon, PaidMenuButtons)
from loader import payment as PaymentCredentials
from payment_services import generate_payment_link
from payment_services.user_data_type import user_data
from states import FSMCalendar

calendarHandlerRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.calendar_menu.name}


@calendarHandlerRouter.callback_query(
    F.data.in_(
        [
            CalendarMenuButtons.CalculateMoneyCalendar.name,
            CalendarActionMenuButtons.CalendarEditData.name,
        ]
    ),
    flags=flags,
)
async def enter_full_name(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(text=CommonLexicon.enter_fio)
    await state.set_state(FSMCalendar.enter_date)


@calendarHandlerRouter.message(
    FSMCalendar.enter_date, 
    flags=flags
)
async def enter_birthday(message: Message, state: FSMContext) -> None:
    if message.text is None:
        return

    fio: str = message.text
    await state.set_data({"fio": fio})

    await message.answer(text=CommonLexicon.enter_date)
    await state.set_state(FSMCalendar.select_month)


@calendarHandlerRouter.message(
    FSMCalendar.select_month,
    DateFilter(is_date=True),
    AgeFilter(is_age=True),
    flags=flags,
)
async def select_month(message: Message, state: FSMContext) -> None:
    if message.text == None or message.from_user == None:
        return
    data = await state.get_data()
    current, next, keyboard = get_data_by_month_for_a_calendar().values()
    birthday: str = message.text
    data.update({"birthday": birthday})
    data.update({"month": {"CurrentMonth": current, "NextMonth": next}})
    await state.update_data(data)

    if not isinstance(keyboard, InlineKeyboardMarkup):
        return
    await message.answer(text=CalendarLexicon.select_month, reply_markup=keyboard)
    await state.set_state(FSMCalendar.check_data)


@calendarHandlerRouter.callback_query(
    FSMCalendar.check_data,
    F.data.in_(
        [
            CalendarSelectMonthMenuButtons.CurrentMonth.name,
            CalendarSelectMonthMenuButtons.NextMonth.name,
        ]
    ),
    flags=flags,
)
async def check_data(callback: CallbackQuery, state: FSMContext) -> None:
    message = callback.message
    if callback.data == None:
        return
    if message == None:
        return

    month = CalendarSelectMonthMenuButtons[callback.data].value
    data = await state.get_data()
    fio: str = data["fio"]
    birthday: str = data["birthday"]
    data.update({"month": data["month"][callback.data]})
    await state.update_data(data)

    await message.answer(text=CommonLexicon.check_data)
    await message.answer(text=f"{CommonLexicon.fio}{fio}")
    await message.answer(text=f"{CommonLexicon.birthday}{birthday}")
    await message.answer(text=f"{CommonLexicon.current_month}{month}")
    await message.answer(
        text=CommonLexicon.selected_action, reply_markup=calendar_action_menu_keyboard
    )


@calendarHandlerRouter.message(
    FSMCalendar.check_data,
    DateFilter(is_date=True),
    flags=flags,
)
async def wrong_age(message: Message) -> None:
    if message.text == None:
        return

    await message.reply(CommonLexicon.legal_age)


@calendarHandlerRouter.message(
    FSMCalendar.check_data, 
    flags=flags
)
async def wrong_input(message: Message) -> None:
    if message.text == None:
        return

    await message.reply(CommonLexicon.invalid_format_date)


@calendarHandlerRouter.callback_query(
    F.data == CalendarActionMenuButtons.CalendarConfirmData.name, flags=flags
)
async def order(callback: CallbackQuery, state: FSMContext):
    callback.answer()
    message = callback.message
    data: dict = await state.get_data()
    if message == None or message.from_user == None:
        return

    user_data["chat_id"] = message.chat.id
    user_data["user_id"] = message.from_user.id
    user_data["service_species"] = PaidMenuButtons.MoneyCalendar.name
    user_data["fio"] = data["fio"]
    user_data["month"] = data["month"].isoformat()
    user_data["birthday"] = data["birthday"]
    link = generate_payment_link(
        cost=Decimal(f"{PaymentCredentials.price.money_calendar}.00"),
        number=random.randint(10**6, (10**7) - 1),
        user_data=user_data,
        description=f"Консультация: {PaidMenuButtons.MoneyCalendar.value}",
    )

    await message.answer(
        text=CommonLexicon.pay_message,
        reply_markup=get_payment_keyboard(
            link=link, backbutton=PaidMenuButtons.BackToPaidMenu
        ),
    )
    await state.clear()
