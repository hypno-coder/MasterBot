from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from keyboards import get_main_keyboard 
from lexicon import BotText
from config_data import SpamConfig

router: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.main_menu.name}

@router.message(CommandStart(), flags=flags)
async def process_start_command(message: Message, status: str) -> None:
    print(status)
    await message.answer(text=BotText.main_menu,
                         reply_markup=get_main_keyboard(status))


@router.callback_query(lambda a: a.data == 'BackToMainMenu', flags=flags)
async def back_to_main_menu(callback: CallbackQuery, status: str) -> None:
    if callback.message == None:
        return
    await callback.answer()
    await callback.message.edit_text(text=BotText.main_menu, 
                                           reply_markup=get_main_keyboard(status))

@router.message(Text(text='Проверить подписку 🧙🪄✨'), flags=flags)
async def process_cucumber_answer(message: Message, status: str) -> None:
    await message.answer(text=BotText.sub_main_menu,
                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await message.answer(text=BotText.main_menu,
                         reply_markup=get_main_keyboard(status))


