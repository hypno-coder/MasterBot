from enum import Enum
from typing import Type

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon import PagiLexicon


class Keyboard:
    @staticmethod
    def create_pagi(
        *buttons: str, keyboard: list[InlineKeyboardButton]
    ) -> InlineKeyboardMarkup:
        kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        kb_builder.row(
            *[
                InlineKeyboardButton(
                    text=(
                        getattr(PagiLexicon, button.split("_")[-1])
                        if buttons.index(button) in [0, len(buttons) - 1]
                        else button
                    ),
                    callback_data=button,
                )
                for button in buttons
            ]
        )
        for button in keyboard:
            kb_builder.row(button)
        return kb_builder.as_markup()

    @staticmethod
    def create_inline(
        width: int, keyboard: Type[Enum] | None = None, backButton: Enum | None = None
    ) -> InlineKeyboardMarkup:

        kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

        if keyboard != None:
            for button in keyboard:
                if button.name.startswith("Back"):
                    continue
                kb_builder.add(
                    InlineKeyboardButton(text=button.value, callback_data=button.name)
                )
        if backButton != None:
            kb_builder.row(
                InlineKeyboardButton(
                    text=backButton.value, callback_data=backButton.name
                )
            )
        kb_builder.adjust(width)
        return kb_builder.as_markup()
