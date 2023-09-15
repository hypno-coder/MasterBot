from aiogram.types import InlineKeyboardMarkup

from lexicon import FreeMenuButtons, MainMenuButtons 
from .keyboards_generator import Keyboard 

MENU_ITEMS_PER_ROW = 1

free_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
        MENU_ITEMS_PER_ROW, 
        FreeMenuButtons, 
        MainMenuButtons.BackToMainMenu)

