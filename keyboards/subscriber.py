from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lexicon import MiddlewareButtons 
from loader import config


subscribe_buttons = [
        [InlineKeyboardButton(
            text=MiddlewareButtons.check_sub.value,
            callback_data=MiddlewareButtons.check_sub.name
            )],
        [InlineKeyboardButton(
            text=MiddlewareButtons.subscribe.value,
            url=config.tg_bot.channel_link)]]


subscribe_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=subscribe_buttons)
