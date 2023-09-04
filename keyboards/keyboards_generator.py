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

def create_pagination_keyboard(
        *buttons: str, keyboard: list[InlineKeyboardButton]) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=BotBtnText.find(button.split('_')[-1]) 
        if buttons.index(button) in [0, len(buttons)-1] else button,
        callback_data=button) for button in buttons])
    for button in keyboard:  
        kb_builder.row(button)
    return kb_builder.as_markup()

