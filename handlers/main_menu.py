from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery 

from keyboards import main_menu_keyboard 
from lexicon import CommonLexicon, MainMenuButtons, MiddlewareButtons 
from config_data import SpamConfig

mainMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.main_menu.name}

@mainMenuRouter.message(CommandStart(), flags=flags)
@mainMenuRouter.callback_query(F.data == MainMenuButtons.BackToMainMenu.name, flags=flags)
async def start_main_menu(event: Message | CallbackQuery) -> None:
    if isinstance(event, Message):
        await event.answer(text=CommonLexicon.main_menu,
                         reply_markup=main_menu_keyboard)
        await event.delete()

    elif isinstance(event, CallbackQuery):
        if event.message == None:
            return

        await event.answer()
        event = event.message
        await event.edit_text(text=CommonLexicon.main_menu,
                         reply_markup=main_menu_keyboard)


@mainMenuRouter.callback_query(F.data == MiddlewareButtons.check_sub.name, flags=flags)
async def check_sub(callback: CallbackQuery) -> None:
    if callback.message == None:
        return
    await callback.message.edit_text(text=CommonLexicon.successful_subscription,
                         reply_markup=main_menu_keyboard)

    



