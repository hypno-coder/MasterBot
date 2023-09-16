from lexicon import JantraMenuButtons

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_button_1: InlineKeyboardButton = InlineKeyboardButton(
    text=JantraMenuButtons.CreateJantra.value,
    callback_data=JantraMenuButtons.CreateJantra.name)

sonnik_repeat_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[inline_button_1]])
