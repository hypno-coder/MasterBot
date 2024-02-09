from aiogram import F, Router
from aiogram.types import CallbackQuery

from config_data import SpamConfig
from keyboards import lock_control_menu_keyboard
from lexicon import AdminMenuButtons, LockMenuLexicon
from loader import config

lockControlMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.lock_control_menu.name}


@lockControlMenuRouter.callback_query(
    F.data == AdminMenuButtons.LockControl.name,
    F.from_user.id.in_(config.tg_bot.admin_ids),
)
async def lock_control_menu(callback: CallbackQuery) -> None:
    if callback.message == None:
        return
    await callback.answer()
    message = callback.message
    await message.edit_text(
        text=LockMenuLexicon.bot_access, reply_markup=lock_control_menu_keyboard
    )
