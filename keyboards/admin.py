from aiogram.types import InlineKeyboardMarkup

from lexicon import (AdminMenuButtons, AdminPaidButtons,
                     LockControlMenuButtons)

from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 1

admin_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, keyboard=AdminMenuButtons
)
admin_calculate_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, 
    keyboard=AdminPaidButtons, 
    backButton=AdminMenuButtons.BackToAdminMenu
)

lock_control_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, 
    keyboard=LockControlMenuButtons, 
    backButton=AdminMenuButtons.BackToAdminMenu
)
