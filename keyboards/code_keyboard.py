from aiogram.types import InlineKeyboardMarkup
from keyboards.keyboards_generator import create_inline_kb
from .callback_data import BotCBData

MENU_ITEMS_PER_ROW = 1

CODE_MENU_BUTTONS = (
        BotCBData.MoneyCodeBtn2.name,
        BotCBData.BackToPaidMenu.name,
    )

CODE_ACTION_MENU_BUTTONS = (
        BotCBData.MoneyCodeBtn3.name,
        BotCBData.MoneyCodeBtn4.name,
    )


code_menu_keyboard: InlineKeyboardMarkup = create_inline_kb(MENU_ITEMS_PER_ROW, *CODE_MENU_BUTTONS)    
code_action_menu_keyboard: InlineKeyboardMarkup = create_inline_kb(MENU_ITEMS_PER_ROW, *CODE_ACTION_MENU_BUTTONS)    






