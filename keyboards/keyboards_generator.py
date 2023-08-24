from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import BotBtnText
from .callback_data import BotCBData 


def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if args:
        for btn in args:
            buttons.append(InlineKeyboardButton(
                text=getattr(BotBtnText, btn),
                callback_data=getattr(BotCBData, btn).value
                ))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()
