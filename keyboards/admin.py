from aiogram.types import InlineKeyboardMarkup

from lexicon import AdminMenuButtons, AdminMenuButtons
from .keyboards_generator import Keyboard 

MENU_ITEMS_PER_ROW = 1

admin_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
        MENU_ITEMS_PER_ROW, 
        AdminMenuButtons) 

