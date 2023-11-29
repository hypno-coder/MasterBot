from aiogram import Router, F
from aiogram.types import CallbackQuery 
from aiogram.fsm.context import FSMContext 

from keyboards import sonnik_menu_keyboard 
from lexicon import FreeMenuButtons, SonnikLexicon
from config_data import SpamConfig

sonnikMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.sonnik_menu.name}


@sonnikMenuRouter.callback_query(F.data == FreeMenuButtons.Sonnik.name, flags=flags)
async def sonnik_menu(callback: CallbackQuery) -> None:
    if callback.message == None:
        return

    await callback.message.edit_text(text=SonnikLexicon.description, reply_markup=sonnik_menu_keyboard)
 
