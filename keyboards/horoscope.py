from aiogram.types import InlineKeyboardMarkup

from lexicon import (ActionChooseGenderButtons, CompareZodiacButtons,
                     MainMenuButtons, GetCompareZodiacButtons,
                     UnitedZodiacButtons, ZodiacButtons)

from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 3
MNU_ITEMS_FIRST_LINE = 4


zodiac_menu: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW,
    keyboard=ZodiacButtons,
    backButton=MainMenuButtons.BackToMainMenu,
)

active_zodiac_menu: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW,
    MNU_ITEMS_FIRST_LINE,
    keyboard=UnitedZodiacButtons,
    backButton=MainMenuButtons.BackToMainMenu,
)


MENU_ITEMS_PER_ROW = 2
gender_compare_menu: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW,
    keyboard=ActionChooseGenderButtons,
    backButton=MainMenuButtons.BackToMainMenu,
)


MENU_ITEMS_PER_ROW = 1
action_zodiac_compare_menu: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW,
    keyboard=CompareZodiacButtons,
    backButton=MainMenuButtons.BackToMainMenu,
)

MENU_ITEMS_PER_ROW = 1
get_zodiac_compare_menu: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW,
    keyboard=GetCompareZodiacButtons,
    backButton=MainMenuButtons.BackToMainMenu,
)
