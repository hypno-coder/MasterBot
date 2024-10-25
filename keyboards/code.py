from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon import CodeMenuButtons, CodeActionMenuButtons, PaidMenuButtons
from .keyboards_generator import Keyboard 

MENU_ITEMS_PER_ROW = 1

code_action_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
        MENU_ITEMS_PER_ROW, keyboard=CodeActionMenuButtons) 

code_menu_buttons = [
        InlineKeyboardButton(
            text=CodeMenuButtons.CalculateMoneyCode.value,
            callback_data=CodeMenuButtons.CalculateMoneyCode.name
            ),
        InlineKeyboardButton(
            text=PaidMenuButtons.BackToPaidMenu.value,
            callback_data=PaidMenuButtons.BackToPaidMenu.name
            )
        ]



