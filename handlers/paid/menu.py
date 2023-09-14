from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery 

from keyboards import paid_menu_keyboard 
from lexicon import MainMenuButtons, PaidMenuButtons, CommonLexicon 
from config_data import SpamConfig

menuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.paid_menu.name}


@menuRouter.callback_query(F.data.in_([MainMenuButtons.PaidServices.name,
                                       PaidMenuButtons.BackToPaidMenu.name]), flags=flags)
async def start_paid_menu(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    if isinstance(event, Message):
        await event.answer(text=CommonLexicon.paid_menu,
                         reply_markup=paid_menu_keyboard)
        await event.delete()

    elif isinstance(event, CallbackQuery):
        if event.message == None:
            return

        await event.answer()
        event = event.message
        await event.edit_text(text=CommonLexicon.paid_menu,
                         reply_markup=paid_menu_keyboard)
