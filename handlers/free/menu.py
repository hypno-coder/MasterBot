from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config_data import SpamConfig
from keyboards import free_menu_keyboard
from lexicon import FreeMenuButtons, FreeMenuLexicon, MainMenuButtons

menuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.free_menu.name}


@menuRouter.callback_query(
    F.data.in_(
        [MainMenuButtons.FreeServices.name, FreeMenuButtons.BackToFreeMenu.name]
    ),
    flags=flags,
)
async def start_free_menu(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    if isinstance(event, Message):
        await event.answer(
            text=FreeMenuLexicon.services, reply_markup=free_menu_keyboard
        )
        await event.delete()

    elif isinstance(event, CallbackQuery):
        if event.message == None:
            return

        await event.answer()
        message = event.message
        await message.edit_text(
            text=FreeMenuLexicon.services, reply_markup=free_menu_keyboard
        )
