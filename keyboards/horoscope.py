from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_zodiac_keyboard() -> None:
    keyboard_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Овен', callback_data='Aries')
    keyboard_builder.button(text=' ', callback_data='')
    keyboard_builder.button(text=' ', callback_data='')
    keyboard_builder.button(text=' ', callback_data='')
    keyboard_builder.button(text=' ', callback_data='')
    keyboard_builder.button(text=' ', callback_data='')
    keyboard_builder.button(text=' ', callback_data='')
    keyboard_builder.button(text=' ', callback_data='')
    keyboard_builder.button(text=' ', callback_data='')
    keyboard_builder.button(text=' ', callback_data='')
    keyboard_builder.button(text=' ', callback_data='')
    keyboard_builder.button(text=' ', callback_data='')
    keyboard_builder.button(text=' ', callback_data='')
    keyboard_builder.button(text=' ', callback_data='')
    keyboard_builder.button(text=' ', callback_data='')
    
