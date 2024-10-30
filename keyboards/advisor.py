from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon import (AdvisorActionMenuButtons, AdvisorMenuButtons,
                     MainMenuButtons)

from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 1

advisor_action_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, 
    keyboard=AdvisorActionMenuButtons, 
    backButton=MainMenuButtons.BackToMainMenu
)

advisor_menu_buttons = [
    InlineKeyboardButton(
        text=AdvisorMenuButtons.AskAnAdvisorAQuestion.value,
        callback_data=AdvisorMenuButtons.AskAnAdvisorAQuestion.name,
    ),
    InlineKeyboardButton(
        text=MainMenuButtons.BackToMainMenu.value,
        callback_data=MainMenuButtons.BackToMainMenu.name,
    ),
]
