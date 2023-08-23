from aiogram.types import InlineKeyboardMarkup
from keyboards.keyboards_generator import create_inline_kb
from .callback_data import BotCBData

ROW_COUNT = 1 
PAID_KEYBOARD_BUTTONS = (
        BotCBData.Btn1.name,
        BotCBData.MoneyCodeBtn1.name,
    )



paid_menu_keyboard: InlineKeyboardMarkup = create_inline_kb(ROW_COUNT, *PAID_KEYBOARD_BUTTONS)    
