from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery 

from keyboards import paid_menu_keyboard, BotCBData
from lexicon import BotText 
from utils import remove_message
from config_data import SpamConfig

menuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.paid_menu.name}

@menuRouter.message(CommandStart(), flags=flags)
async def start_paid_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    reply = await message.answer(text=BotText.paid_menu,
                         reply_markup=paid_menu_keyboard)

    await message.delete()
    await remove_message(chat_id=message.chat.id, message_id=reply.message_id)

@menuRouter.callback_query(lambda a: a.data == BotCBData.BackToPaidMenu.value, flags=flags)
async def back_to_paid_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    if callback.message == None:
        return
    await callback.answer()
    await callback.message.edit_text(text=BotText.paid_menu, 
                                           reply_markup=paid_menu_keyboard)

    await remove_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
