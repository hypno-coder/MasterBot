from aiogram.types import InlineKeyboardMarkup
from keyboards.keyboards_generator import create_inline_kb
from .callback_data import BotCBData

MENU_ITEMS_PER_ROW = 2
FREE_KEYBOARD_BUTTONS = (
        BotCBData.Btn2.name,
        BotCBData.Btn3.name,
        BotCBData.Btn4.name,
        BotCBData.Btn5.name,
        BotCBData.Btn6.name,
    )



free_menu_keyboard: InlineKeyboardMarkup = create_inline_kb(MENU_ITEMS_PER_ROW, *FREE_KEYBOARD_BUTTONS)    
