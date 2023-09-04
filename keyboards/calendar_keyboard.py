from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.keyboards_generator import create_inline_kb
from lexicon import BotBtnText
from .callback_data import BotCBData

MENU_ITEMS_PER_ROW = 1

CALENDAR_ACTION_MENU_BUTTONS = (
        BotCBData.MoneyCalendarBtn2.name,
        BotCBData.MoneyCalendarBtn4.name,
    )

calendar_menu_keyboard = [
        InlineKeyboardButton(
            text=BotBtnText.MoneyCalendarBtn2,
            callback_data=BotCBData.MoneyCalendarBtn2.value
            ),
        InlineKeyboardButton(
            text=BotBtnText.BackToPaidMenu,
            callback_data=BotCBData.BackToPaidMenu.value
            )
        ]

calendar_action_menu_keyboard: InlineKeyboardMarkup = create_inline_kb(MENU_ITEMS_PER_ROW, *CALENDAR_ACTION_MENU_BUTTONS)    



