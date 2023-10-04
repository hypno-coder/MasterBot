from enum import Enum
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lexicon import CommonMenuButtons  


def get_payment_keyboard(link: str, backbutton: Enum) -> InlineKeyboardMarkup:
    buttons = [
            [InlineKeyboardButton(
                text=CommonMenuButtons.payment,
                url=link)],
            [InlineKeyboardButton(
                text=backbutton.value,
                callback_data=backbutton.name)]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
