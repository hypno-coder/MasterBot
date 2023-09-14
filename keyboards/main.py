from aiogram.types import InlineKeyboardMarkup

from lexicon import MainMenuButtons 
from .keyboards_generator import create_inline_keyboard

MENU_ITEMS_PER_ROW = 1

main_menu_keyboard: InlineKeyboardMarkup = create_inline_keyboard(
        MENU_ITEMS_PER_ROW, 
        MainMenuButtons)

