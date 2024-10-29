from enum import Enum

from aiogram.types import InlineKeyboardMarkup

from lexicon import (ActionChooseGenderButtons, CompareZodiacButtons,
                     FreeMenuButtons, GetCompareZodiacButtons,
                     UnitedZodiacButtons, ZodiacButtons)

from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 3
MNU_ITEMS_FIRST_LINE = 4


zodiac_menu: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW,
    keyboard=ZodiacButtons,
    backButton=FreeMenuButtons.BackToFreeMenu,
)

active_zodiac_menu: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW,
    MNU_ITEMS_FIRST_LINE,
    keyboard=UnitedZodiacButtons,
    backButton=FreeMenuButtons.BackToFreeMenu,
)


MENU_ITEMS_PER_ROW = 2
gender_compare_menu: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW,
    keyboard=ActionChooseGenderButtons,
    backButton=FreeMenuButtons.BackToFreeMenu,
)


MENU_ITEMS_PER_ROW = 1
action_zodiac_compare_menu: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW,
    keyboard=CompareZodiacButtons,
    backButton=FreeMenuButtons.BackToFreeMenu,
)

MENU_ITEMS_PER_ROW = 1
get_zodiac_compare_menu: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW,
    keyboard=GetCompareZodiacButtons,
    backButton=FreeMenuButtons.BackToFreeMenu,
)
