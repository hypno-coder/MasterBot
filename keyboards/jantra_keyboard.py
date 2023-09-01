from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import BotBtnText
from .callback_data import BotCBData
from keyboards.keyboards_generator import create_inline_kb


jantra_menu_keyboard = [
        InlineKeyboardButton(
            text=BotBtnText.JantraBtn2,
            callback_data=BotCBData.JantraBtn2.value
            ),
        InlineKeyboardButton(
            text=BotBtnText.BackToPaidMenu,
            callback_data=BotCBData.BackToPaidMenu.value
            )

        ]

def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=BotBtnText.find(button) if BotBtnText.find(button) else button,
        callback_data=button) for button in buttons])
    kb_builder.row(*jantra_menu_keyboard)
    return kb_builder.as_markup()


MENU_ITEMS_PER_ROW = 1

JANTRA_ACTION_MENU_BUTTONS = (
        BotCBData.JantraBtn3.name,
        BotCBData.JantraBtn4.name,
    )

jantra_action_menu_keyboard: InlineKeyboardMarkup = create_inline_kb(MENU_ITEMS_PER_ROW, *JANTRA_ACTION_MENU_BUTTONS)    


