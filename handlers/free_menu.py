from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from keyboards import free_menu_keyboard 
from lexicon import BotText
from config_data import SpamConfig

router: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.free_menu.name}

@router.message(CommandStart(), flags=flags)
async def process_start_command(message: Message) -> None:
    await message.answer(text=BotText.free_menu,
                         reply_markup=free_menu_keyboard)


@router.callback_query(lambda a: a.data == 'BackToFreeMenu', flags=flags)
async def back_to_free_menu(callback: CallbackQuery) -> None:
    if callback.message == None:
        return
    await callback.answer()
    await callback.message.edit_text(text=BotText.free_menu, 
                                           reply_markup=free_menu_keyboard)

@router.message(Text(text='Проверить подписку 🧙🪄✨'), flags=flags)
async def process_cucumber_answer(message: Message) -> None:
    await message.answer(text=BotText.sub_free_menu,
                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await message.answer(text=BotText.free_menu,
                         reply_markup=free_menu_keyboard)


