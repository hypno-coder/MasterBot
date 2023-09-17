from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon import AdvisorMenuButtons, AdvisorActionMenuButtons, FreeMenuButtons
from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 1

advisor_action_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
        MENU_ITEMS_PER_ROW, AdvisorActionMenuButtons) 

advisor_menu_buttons = [
        InlineKeyboardButton(
            text=AdvisorMenuButtons.AskAnAdvisorAQuestion.value,
            callback_data=AdvisorMenuButtons.AskAnAdvisorAQuestion.name
            ),
        InlineKeyboardButton(
            text=FreeMenuButtons.BackToFreeMenu.value,
            callback_data=FreeMenuButtons.BackToFreeMenu.name
            )
        ]


