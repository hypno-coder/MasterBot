from aiogram.types import InlineKeyboardMarkup
from enum import Enum

from lexicon import ZodiacButtons, FreeMenuButtons, UnitedZodiacButtons 
from .keyboards_generator import Keyboard 

MENU_ITEMS_PER_ROW = 3
MNU_ITEMS_FIRST_LINE = 4


zodiac_menu: InlineKeyboardMarkup = Keyboard.create_inline(
        MENU_ITEMS_PER_ROW, 
        keyboard=ZodiacButtons, 
        backButton=FreeMenuButtons.BackToFreeMenu)

active_zodiac_menu: InlineKeyboardMarkup = Keyboard.create_inline(
        MENU_ITEMS_PER_ROW, 
        MNU_ITEMS_FIRST_LINE,
        keyboard=UnitedZodiacButtons, 
        backButton=FreeMenuButtons.BackToFreeMenu)
