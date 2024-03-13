from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config_data import SpamConfig
from keyboards import admin_access_keyboard, main_menu_keyboard
from lexicon import MainMenuButtons, MainMenuLexicon, MiddlewareButtons
from lexicon.admin_menu.lexicon import LockMenuLexicon
from loader import config

mainMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.main_menu.name}


@mainMenuRouter.message(CommandStart(), flags=flags)
@mainMenuRouter.callback_query(
    F.data == MainMenuButtons.BackToMainMenu.name, flags=flags
)
async def start_main_menu(
    event: Message | CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.clear()
    chat_id = ""
   
    if isinstance(event, Message):
        chat_id = event.chat.id
        await event.answer(
            text=MainMenuLexicon.select_features, reply_markup=main_menu_keyboard
        )
        await event.delete()

    elif isinstance(event, CallbackQuery):
        if event.message == None:
            return

        chat_id = event.message.chat.id
        await event.answer()
        event = event.message
        await event.edit_text(
            text=MainMenuLexicon.select_features, reply_markup=main_menu_keyboard
        )
    if event.from_user == None:
        return
    
    if event.from_user.id in config.tg_bot.admin_ids:
        await bot.send_message(
            chat_id=chat_id,
            text=LockMenuLexicon.admin_access,
            reply_markup=admin_access_keyboard,
        )


@mainMenuRouter.callback_query(F.data == MiddlewareButtons.check_sub.name, flags=flags)
async def check_sub(callback: CallbackQuery) -> None:
    if callback.message == None:
        return
    await callback.message.edit_text(
        text=MainMenuLexicon.successful_subscription, reply_markup=main_menu_keyboard
    )
    await callback.answer(text=MainMenuLexicon.gratitude, show_alert=True)
