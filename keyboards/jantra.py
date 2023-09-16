from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon import JantraMenuButtons, JantraActionMenuButtons, PaidMenuButtons
from .keyboards_generator import Keyboard 

MENU_ITEMS_PER_ROW = 1

jantra_action_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
        MENU_ITEMS_PER_ROW, JantraActionMenuButtons) 

jantra_menu_buttons = [
        InlineKeyboardButton(
            text=JantraMenuButtons.CreateJantra.value,
            callback_data=JantraMenuButtons.CreateJantra.name
            ),
        InlineKeyboardButton(
            text=PaidMenuButtons.BackToPaidMenu.value,
            callback_data=PaidMenuButtons.BackToPaidMenu.name
            )
        ]



