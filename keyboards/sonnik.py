from lexicon import SonnikActionMenuButtons, SonnikMenuButtons

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon import MainMenuButtons 

repeat_button_1: InlineKeyboardButton = InlineKeyboardButton(
    text=SonnikActionMenuButtons.Repeat.value,
    callback_data=SonnikActionMenuButtons.Repeat.name)
repeat_button_2: InlineKeyboardButton = InlineKeyboardButton(
    text=MainMenuButtons.BackToMainMenu.value,
    callback_data=MainMenuButtons.BackToMainMenu.name)
sonnik_repeat_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[repeat_button_1], [repeat_button_2]])



menu_button_1: InlineKeyboardButton = InlineKeyboardButton(
            text=SonnikMenuButtons.GetSonnik.value,
            callback_data=SonnikMenuButtons.GetSonnik.name)
menu_button_2: InlineKeyboardButton = InlineKeyboardButton(
            text=MainMenuButtons.BackToMainMenu.value,
            callback_data=MainMenuButtons.BackToMainMenu.name)
sonnik_menu_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[menu_button_1], [menu_button_2]])

