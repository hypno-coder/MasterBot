from aiogram.types import InlineKeyboardMarkup

from lexicon import MainMenuButtons, PaidMenuButtons

from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 1

paid_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, PaidMenuButtons, MainMenuButtons.BackToMainMenu
)
