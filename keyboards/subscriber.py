from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import config

inline_button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='Подписаться',
    url=config.tg_bot.channel_link)

subscriber_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[inline_button_1]])

