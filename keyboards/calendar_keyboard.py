from aiogram.types import InlineKeyboardMarkup
from keyboards.keyboards_generator import create_inline_kb
from .callback_data import BotCBData

MENU_ITEMS_PER_ROW = 1
CALENDAR_MENU_BUTTONS = (
        BotCBData.MoneyCalendarBtn2.name,
        BotCBData.BackToPaidMenu.name,
    )

CALENDAR_ACTION_MENU_BUTTONS = (
        BotCBData.MoneyCalendarBtn2.name,
        BotCBData.MoneyCalendarBtn4.name,
    )


calendar_menu_keyboard: InlineKeyboardMarkup = create_inline_kb(MENU_ITEMS_PER_ROW, *CALENDAR_MENU_BUTTONS)    
calendar_action_menu_keyboard: InlineKeyboardMarkup = create_inline_kb(MENU_ITEMS_PER_ROW, *CALENDAR_ACTION_MENU_BUTTONS)    



