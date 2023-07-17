from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.keyboards_generator import create_inline_kb
from lexicon import BotBtnText
from .callback_data import BotCBData


__code_button: InlineKeyboardButton = InlineKeyboardButton(
            text='Приобрести Кoд',
            callback_data='Huyak_Cod'
            )

code_menu_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[__code_button]], 
    )


