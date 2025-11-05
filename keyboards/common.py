from aiogram.types import InlineKeyboardMarkup

from lexicon import ActionChooseGenderButtons, ActionChoosePaymentButtons

from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 1


choose_gender_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, keyboard=ActionChooseGenderButtons
)

choose_payment_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, keyboard=ActionChoosePaymentButtons
)

def create_common_keyboard(keyboard, backButton = None):
    return Keyboard.create_inline(
        MENU_ITEMS_PER_ROW,
        keyboard=keyboard,
        backButton=backButton
    )
