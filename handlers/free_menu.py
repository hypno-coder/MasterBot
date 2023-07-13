from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery 

from keyboards import free_menu_keyboard, BotCBData
from lexicon import BotText, BotBtnText
from utils import remove_message
from config_data import SpamConfig

router: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.free_menu.name}

@router.message(Text(text=BotBtnText.Free), flags=flags)
async def start_free_menu(message: Message) -> None:
    reply = await message.answer(text=BotText.free_menu,
                         reply_markup=free_menu_keyboard)
    await remove_message(chat_id=message.chat.id, message_id=reply.message_id)



@router.callback_query(lambda a: a.data == BotCBData.BackFreeMenu.name, flags=flags)
async def back_to_free_menu(callback: CallbackQuery) -> None:
    if callback.message == None:
        return
    await callback.answer()
    await callback.message.edit_text(text=BotText.free_menu, 
                                           reply_markup=free_menu_keyboard)


