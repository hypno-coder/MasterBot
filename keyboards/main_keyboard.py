from aiogram.types import InlineKeyboardMarkup
from keyboards.keyboards_generator import create_inline_kb
from .callback_data import BotCallbackData
from states import UserStatus

ROW_COUNT = 2 
MAIN_KEYBOARD_BUTTONS_FREE = (
        BotCallbackData.Btn3.name,
        BotCallbackData.Btn4.name,
        BotCallbackData.Btn5.name,
        BotCallbackData.Btn6.name,
    )
MAIN_KEYBOARD_BUTTONS_PREM = (
        BotCallbackData.Btn1.name,
        BotCallbackData.Btn2.name,
        BotCallbackData.Btn3.name,
        BotCallbackData.Btn4.name,
        BotCallbackData.Btn5.name,
        BotCallbackData.Btn6.name,
        BotCallbackData.Btn7.name,
    )



def get_main_keyboard(status: str = UserStatus.FREE.value) -> InlineKeyboardMarkup | None:
    if status == UserStatus.FREE.value:
        return create_inline_kb(ROW_COUNT, *MAIN_KEYBOARD_BUTTONS_FREE)    
    if status == UserStatus.PREMIUM.value or status == UserStatus.ADMIN.value:
        return create_inline_kb(ROW_COUNT, *MAIN_KEYBOARD_BUTTONS_PREM)    
