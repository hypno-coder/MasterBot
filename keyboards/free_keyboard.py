from aiogram.types import InlineKeyboardMarkup
from keyboards.keyboards_generator import create_inline_kb
from .callback_data import BotCallbackData

ROW_COUNT = 2 
FREE_KEYBOARD_BUTTONS = (
        BotCallbackData.Btn1.name,
        BotCallbackData.Btn2.name,
        BotCallbackData.Btn3.name,
        BotCallbackData.Btn4.name,
        BotCallbackData.Btn5.name,
        BotCallbackData.Btn6.name,
        BotCallbackData.Btn7.name,
    )



free_menu_keyboard: InlineKeyboardMarkup = create_inline_kb(ROW_COUNT, *FREE_KEYBOARD_BUTTONS)    
