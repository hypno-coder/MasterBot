from aiogram.types import InlineKeyboardMarkup

from lexicon import ActionChooseGenderButtons

from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 1


choose_gender_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, keyboard=ActionChooseGenderButtons
)
