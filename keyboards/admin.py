from aiogram.types import InlineKeyboardMarkup

from lexicon import AdminMenuButtons, LockControlMenuButtons

from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 1

admin_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, AdminMenuButtons
)


lock_control_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, LockControlMenuButtons, AdminMenuButtons.BackToAdminMenu
)
