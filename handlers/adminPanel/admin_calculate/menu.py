from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config_data import SpamConfig
from keyboards import admin_calculate_menu_keyboard
from lexicon import AdminMenuButtons, AdminMenuLexicon, AdminPaidButtons
from loader import config

adminCalcMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.paid_menu.name}


@adminCalcMenuRouter.callback_query(
    F.data.in_(
        [
            AdminMenuButtons.AdminCalculation.name,
            AdminPaidButtons.BackToAdminPaidMenu.name,
        ]
    ),
    F.from_user.id.in_(config.tg_bot.admin_ids),
    flags=flags,
)
async def admin_calck_menu(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    if isinstance(event, Message):
        await event.answer(
            text=AdminMenuLexicon.services, reply_markup=admin_calculate_menu_keyboard
        )
        await event.delete()

    elif isinstance(event, CallbackQuery):
        if event.message == None:
            return

        await event.answer()
        message = event.message
        await message.edit_text(
            text=AdminMenuLexicon.services, reply_markup=admin_calculate_menu_keyboard
        )
