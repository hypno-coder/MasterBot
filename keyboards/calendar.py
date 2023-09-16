from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon import CalendarMenuButtons, CalendarActionMenuButtons, PaidMenuButtons
from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 1

calendar_action_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
        MENU_ITEMS_PER_ROW, CalendarActionMenuButtons) 

calendar_menu_buttons = [
        InlineKeyboardButton(
            text=CalendarMenuButtons.CalculateMoneyCalendar.value,
            callback_data=CalendarMenuButtons.CalculateMoneyCalendar.name
            ),
        InlineKeyboardButton(
            text=PaidMenuButtons.BackToPaidMenu.value,
            callback_data=PaidMenuButtons.BackToPaidMenu.name
            )
        ]


