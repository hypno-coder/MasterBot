from lexicon.buttons import BotBtnText
from loader import config
from lexicon import BotBtnText

from aiogram.types import (
        InlineKeyboardButton, 
        InlineKeyboardMarkup,
        KeyboardButton,
        ReplyKeyboardMarkup,
        )

inline_button_1: InlineKeyboardButton = InlineKeyboardButton(
    text=BotBtnText.Sub,
    url=config.tg_bot.channel_link)
sub_inline_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[inline_button_1]], 
    )

common_button_1: KeyboardButton = KeyboardButton(text=BotBtnText.CheckSub)
sub_common_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[common_button_1]], 
                                    resize_keyboard=True)

