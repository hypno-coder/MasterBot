from aiogram.types import InlineKeyboardMarkup

from lexicon import ZodiacButtons, FreeMenuButtons 
from .keyboards_generator import create_inline_keyboard

MENU_ITEMS_PER_ROW = 3

zodiac_menu: InlineKeyboardMarkup = create_inline_keyboard(
        MENU_ITEMS_PER_ROW, 
        ZodiacButtons, 
        FreeMenuButtons.BackToFreeMenu)

