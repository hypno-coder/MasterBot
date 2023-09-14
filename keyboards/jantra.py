from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lexicon import BotBtnText, PaidMenuButtons
from .callback_data import BotCBData 
from keyboards.keyboards_generator import create_inline_kb

MENU_ITEMS_PER_ROW = 1

JANTRA_ACTION_MENU_BUTTONS = (
        BotCBData.JantraBtn3.name,
        BotCBData.JantraBtn4.name,
    )

jantra_menu_keyboard = [
        InlineKeyboardButton(
            text=BotBtnText.JantraBtn2,
            callback_data=BotCBData.JantraBtn2.value
            ),
        InlineKeyboardButton(
            text=PaidMenuButtons.BackToPaidMenu.value,
            callback_data=PaidMenuButtons.BackToPaidMenu.name
            )

        ]

jantra_action_menu_keyboard: InlineKeyboardMarkup = create_inline_kb(MENU_ITEMS_PER_ROW, *JANTRA_ACTION_MENU_BUTTONS)    


