from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery 

from keyboards import free_menu_keyboard
from lexicon import FreeMenuButtons, MainMenuButtons, FreeMenuLexicon
from config_data import SpamConfig

menuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.free_menu.name}


@menuRouter.callback_query(F.data.in_([MainMenuButtons.FreeServices.name,
                                       FreeMenuButtons.BackToFreeMenu.name]), flags=flags)
async def start_free_menu(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    if isinstance(event, Message):
        await event.answer(text=FreeMenuLexicon.services,
                         reply_markup=free_menu_keyboard)
        await event.delete()

    elif isinstance(event, CallbackQuery):
        if event.message == None:
            return

        await event.answer()
        message = event.message
        await message.edit_text(text=FreeMenuLexicon.services,
                         reply_markup=free_menu_keyboard)
