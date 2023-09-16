from aiogram.types import InlineKeyboardMarkup

from lexicon import MainMenuButtons 
from .keyboards_generator import Keyboard 

MENU_ITEMS_PER_ROW = 1

main_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
        MENU_ITEMS_PER_ROW, 
        MainMenuButtons)

