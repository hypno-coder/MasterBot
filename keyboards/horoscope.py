from aiogram.types import InlineKeyboardMarkup

from lexicon import ZodiacButtons, FreeMenuButtons 
from .keyboards_generator import Keyboard 

MENU_ITEMS_PER_ROW = 3

zodiac_menu: InlineKeyboardMarkup = Keyboard.create_inline(
        MENU_ITEMS_PER_ROW, 
        ZodiacButtons, 
        FreeMenuButtons.BackToFreeMenu)

