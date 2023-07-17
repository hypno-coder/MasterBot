from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import BotBtnText
from .callback_data import BotCBData


jantra_menu_keyboard = [
        InlineKeyboardButton(
            text=BotBtnText.Btn11,
            callback_data=BotCBData.Btn11.value
            ),
        InlineKeyboardButton(
            text=BotBtnText.BackPaidMenu,
            callback_data=BotCBData.BackPaidMenu.value
            )

        ]

def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=BotBtnText.find(button) if BotBtnText.find(button) else button,
        callback_data=button) for button in buttons])
    kb_builder.row(*jantra_menu_keyboard)
    return kb_builder.as_markup()


