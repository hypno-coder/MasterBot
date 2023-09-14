from aiogram.types import InlineKeyboardMarkup

from lexicon import FreeMenuButtons, MainMenuButtons 
from .keyboards_generator import create_inline_keyboard

MENU_ITEMS_PER_ROW = 1

free_menu_keyboard: InlineKeyboardMarkup = create_inline_keyboard(
        MENU_ITEMS_PER_ROW, 
        FreeMenuButtons, 
        MainMenuButtons.BackToMainMenu)

