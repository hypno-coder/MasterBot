from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 
from lexicon import BotBtnText, BotText


btn_1: KeyboardButton = KeyboardButton(text=BotBtnText.Free)
btn_2: KeyboardButton = KeyboardButton(text=BotBtnText.Paid)

main_menu_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[btn_1, btn_2]],
                                    resize_keyboard=True,
                                    input_field_placeholder=BotText.main_menu_placeholder)
