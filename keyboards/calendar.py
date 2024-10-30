from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon import (CalendarActionMenuButtons, CalendarMenuButtons,
                     CalendarSelectMonthMenuButtons, PaidMenuButtons)

from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 1

calendar_action_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, keyboard=CalendarActionMenuButtons
)

calendar_menu_buttons = [
    InlineKeyboardButton(
        text=CalendarMenuButtons.CalculateMoneyCalendar.value,
        callback_data=CalendarMenuButtons.CalculateMoneyCalendar.name,
    ),
    InlineKeyboardButton(
        text=PaidMenuButtons.BackToPaidMenu.value,
        callback_data=PaidMenuButtons.BackToPaidMenu.name,
    ),
]


def get_current_and_next_months() -> tuple[datetime, datetime]:
    now = datetime.now()
    current_month_date = datetime(now.year, now.month, 1)
    if now.month == 12:
        next_month_date = datetime(now.year + 1, 1, 1)
    else:
        next_month_date = datetime(now.year, now.month + 1, 1)
    return current_month_date, next_month_date


def get_data_by_month_for_a_calendar() -> dict[str, datetime | InlineKeyboardMarkup]:
    current, next = get_current_and_next_months()
    CalendarSelectMonthMenuButtons.set_dynamic_values(current, next)
    month_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
        MENU_ITEMS_PER_ROW, keyboard=CalendarSelectMonthMenuButtons
    )
    return {"current": current, "next": next, "keyboard": month_keyboard}
