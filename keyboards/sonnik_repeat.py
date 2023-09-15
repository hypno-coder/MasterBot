from lexicon import BotBtnText
from keyboards import BotCBData

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_button_1: InlineKeyboardButton = InlineKeyboardButton(
    text=BotBtnText.Btn2_1,
    callback_data=BotCBData.Btn2.value)

sonnik_repeat_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[inline_button_1]], 
    )
