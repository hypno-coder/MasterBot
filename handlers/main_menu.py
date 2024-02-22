from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config_data import SpamConfig
from keyboards import main_menu_keyboard
from lexicon import MainMenuButtons, MainMenuLexicon, MiddlewareButtons

mainMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.main_menu.name}


@mainMenuRouter.message(CommandStart(), flags=flags)
@mainMenuRouter.callback_query(
    F.data == MainMenuButtons.BackToMainMenu.name, flags=flags
)
async def start_main_menu(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    if isinstance(event, Message):
        await event.answer(
            text=MainMenuLexicon.select_features, reply_markup=main_menu_keyboard
        )
        await event.delete()

    elif isinstance(event, CallbackQuery):
        if event.message == None:
            return

        await event.answer()
        event = event.message
        await event.edit_text(
            text=MainMenuLexicon.select_features, reply_markup=main_menu_keyboard
        )


@mainMenuRouter.callback_query(F.data == MiddlewareButtons.check_sub.name, flags=flags)
async def check_sub(callback: CallbackQuery) -> None:
    if callback.message == None:
        return
    await callback.message.edit_text(
        text=MainMenuLexicon.successful_subscription, reply_markup=main_menu_keyboard
    )
    await callback.answer(text=MainMenuLexicon.gratitude, show_alert=True)
