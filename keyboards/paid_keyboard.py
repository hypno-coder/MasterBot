from aiogram.types import InlineKeyboardMarkup
from keyboards.keyboards_generator import create_inline_kb
from .callback_data import BotCBData

MENU_ITEMS_PER_ROW = 1
PAID_KEYBOARD_BUTTONS = (
        BotCBData.YantraBtn1.name,
        BotCBData.MoneyCodeBtn1.name,
        BotCBData.MoneyCalendarBtn1.name,
    )



paid_menu_keyboard: InlineKeyboardMarkup = create_inline_kb(MENU_ITEMS_PER_ROW, *PAID_KEYBOARD_BUTTONS)    
