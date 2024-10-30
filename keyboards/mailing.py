from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon import MailingActionMenuButtons, MailingButtonMenu

from .keyboards_generator import Keyboard

MENU_ITEMS_PER_ROW = 1

mailing_action_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, keyboard=MailingActionMenuButtons
)

mailing_button_menu_keyboard: InlineKeyboardMarkup = Keyboard.create_inline(
    MENU_ITEMS_PER_ROW, keyboard=MailingButtonMenu
)


def get_mailing_button(button_name, button_link) -> InlineKeyboardMarkup:
    button = [[InlineKeyboardButton(text=button_name, url=button_link)]]
    return InlineKeyboardMarkup(inline_keyboard=button)
