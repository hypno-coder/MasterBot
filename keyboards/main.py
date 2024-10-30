from aiogram.types import (InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup)

from lexicon import MainMenuButtons

from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 1

main_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, keyboard=MainMenuButtons
)

button = KeyboardButton(text="/admin")

admin_access_keyboard = ReplyKeyboardMarkup(
    keyboard=[[button]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
