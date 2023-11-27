from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message 

from keyboards import admin_menu_keyboard 
from lexicon import AdminMenuLexicon 
from config_data import SpamConfig 
from loader import config

adminMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.admin_menu.name}

@adminMenuRouter.message(Command(commands='admin'), F.from_user.id.in_(config.tg_bot.admin_ids))
async def start_admin_menu(event: Message, state: FSMContext) -> None:
    await state.clear()
    await event.answer(text=AdminMenuLexicon.services,
                         reply_markup=admin_menu_keyboard)
    await event.delete()

