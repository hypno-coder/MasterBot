from aiogram.types import InlineKeyboardMarkup
from keyboards.keyboards_generator import create_inline_kb
from .callback_data import BotCBData

MENU_ITEMS_PER_ROW = 1
CODE_KEYBOARD_BUTTONS = (
        BotCBData.MoneyCalendarBtn2.name,
        BotCBData.BackToPaidMenu.name,
    )


calendar_menu_keyboard: InlineKeyboardMarkup = create_inline_kb(MENU_ITEMS_PER_ROW, *CODE_KEYBOARD_BUTTONS)    


