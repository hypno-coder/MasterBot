from lexicon import SonnikActionMenuButtons

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_button_1: InlineKeyboardButton = InlineKeyboardButton(
    text=SonnikActionMenuButtons.Repeat.value,
    callback_data=SonnikActionMenuButtons.Repeat.name)

sonnik_repeat_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[inline_button_1]])
