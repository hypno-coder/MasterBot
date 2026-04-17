from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config_data import SpamConfig
from keyboards import paid_menu_keyboard
from lexicon import ( 
#    MainMenuButtons, 
    PaidMenuButtons, 
    PaidMenuLexicon
)

menuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.paid_menu.name}


@menuRouter.callback_query(
    F.data.in_(
        [
#            MainMenuButtons.PaidServices.name, 
            PaidMenuButtons.BackToPaidMenu.name
        ]
    ),
    flags=flags,
)
async def start_paid_menu(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    if isinstance(event, Message):
        await event.answer(
            text=PaidMenuLexicon.services, reply_markup=paid_menu_keyboard
        )
        await event.delete()

    elif isinstance(event, CallbackQuery):
        if event.message == None:
            return
        await event.answer()
        event = event.message
        await event.edit_text(
            text=PaidMenuLexicon.services, reply_markup=paid_menu_keyboard
        )
