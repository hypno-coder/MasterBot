from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.keyboards_generator import create_inline_kb
from lexicon import BotBtnText, PaidMenuButtons
from .callback_data import BotCBData

MENU_ITEMS_PER_ROW = 1
CODE_ACTION_MENU_BUTTONS = (
        BotCBData.MoneyCodeBtn3.name,
        BotCBData.MoneyCodeBtn4.name,
    )


code_menu_keyboard = [
        InlineKeyboardButton(
            text=BotBtnText.MoneyCodeBtn2,
            callback_data=BotCBData.MoneyCodeBtn2.value
            ),
        InlineKeyboardButton(
            text=PaidMenuButtons.BackToPaidMenu.value,
            callback_data=PaidMenuButtons.BackToPaidMenu.name
            )
        ]



code_action_menu_keyboard: InlineKeyboardMarkup = create_inline_kb(
        MENU_ITEMS_PER_ROW, *CODE_ACTION_MENU_BUTTONS)    






