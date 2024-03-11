from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from config_data import SpamConfig
from keyboards import admin_menu_keyboard
from lexicon import AdminMenuButtons, AdminMenuLexicon
from loader import config

adminMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.admin_menu.name}


@adminMenuRouter.message(
    Command(commands="admin"), F.from_user.id.in_(config.tg_bot.admin_ids)
)
@adminMenuRouter.callback_query(
    F.data == AdminMenuButtons.BackToAdminMenu.name,
    F.from_user.id.in_(config.tg_bot.admin_ids),
    flags=flags,
)
async def admin_menu(
    event: Message | CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await state.clear()
    chat_id = ""

    if isinstance(event, Message):
        chat_id = event.chat.id
        await event.answer(
            text=AdminMenuLexicon.services, reply_markup=admin_menu_keyboard
        )
        await event.delete()

    elif isinstance(event, CallbackQuery):
        if event.message == None:
            return
        chat_id = event.message.chat.id

        await event.answer()
        message = event.message
        await message.edit_text(
            text=AdminMenuLexicon.services, reply_markup=admin_menu_keyboard
        )
    reply = await bot.send_message(
        chat_id=chat_id,
        text="--",
        reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
    )
    await bot.delete_message(chat_id=reply.chat.id, message_id=reply.message_id)
