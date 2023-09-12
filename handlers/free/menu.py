from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery 

from keyboards import free_menu_keyboard
from lexicon import BotText, FreeMenuButtons
from config_data import SpamConfig

menuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.free_menu.name}


@menuRouter.message(CommandStart(), flags=flags)
# @menuRouter.message(Text(text=BotBtnText.Free), flags=flags)
@menuRouter.callback_query(lambda a: a.data == FreeMenuButtons.BackToFreeMenu.name, flags=flags)
async def start_free_menu(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    if isinstance(event, Message):
        await event.answer(text=BotText.free_menu,
                         reply_markup=free_menu_keyboard)
        await event.delete()

    elif isinstance(event, CallbackQuery):
        if event.message == None:
            return

        message = event.message
        await message.edit_text(text=BotText.free_menu,
                         reply_markup=free_menu_keyboard)

