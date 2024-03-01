from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon import (DestinyCardActionMenuButtons, DestinyCardMenuButtons,
                     PaidMenuButtons)

from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 1


destiny_card_action_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, DestinyCardActionMenuButtons
)

destiny_card_menu_buttons = [
    InlineKeyboardButton(
        text=DestinyCardMenuButtons.CalculateDestinyCard.value,
        callback_data=DestinyCardMenuButtons.CalculateDestinyCard.name,
    ),
    InlineKeyboardButton(
        text=PaidMenuButtons.BackToPaidMenu.value,
        callback_data=PaidMenuButtons.BackToPaidMenu.name,
    ),
]
