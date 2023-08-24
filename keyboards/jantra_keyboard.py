from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import BotBtnText
from .callback_data import BotCBData


jantra_menu_keyboard = [
        InlineKeyboardButton(
            text=BotBtnText.YantraBtn2,
            callback_data=BotCBData.YantraBtn2.value
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


