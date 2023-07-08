from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery

from keyboards import main_keyboard 
from lexicon import BotText


router: Router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    await message.answer(text=BotText.main_menu,
                         reply_markup=main_keyboard)


@router.message(Text(text='Проверка 👁'))
@router.callback_query(lambda a: a.data == 'BackToMainMenu')
async def back_to_main_menu(callback: CallbackQuery) -> None:
    if callback.message == None:
        return
    await callback.answer()
    await callback.message.edit_text(text=BotText.main_menu, 
                                           reply_markup=main_keyboard)
