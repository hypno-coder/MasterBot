import re
from aiogram import Router
from aiogram import Bot 
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards import code_menu_keyboard 
from lexicon import BotText, BotBtnText
from config_data import SpamConfig
from states import FSMCode
from filters import DateFilter
from services import calculate_code

codeRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.code_menu.name}

@codeRouter.message(CommandStart(), flags=flags)
async def start_main_menu(message: Message) -> None:
    await message.answer(text='Тут вы можете приобрести денежный код',
                         reply_markup=code_menu_keyboard)

@codeRouter.message(Text(text=BotBtnText.ChekSub), flags=flags)
async def check_sub(message: Message) -> None:
    await message.answer(text="Главное меню",
                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await message.answer(text='Тут вы можете приобрести денежный код',
                         reply_markup=code_menu_keyboard)

@codeRouter.callback_query(lambda a: a.data == "Huyak_Cod", flags=flags)
async def start_sonnik_conv(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    if callback.message == None:
        return
    await state.set_state(FSMCode.calculate_code)
    user_id = callback.from_user.id
    await callback.message.delete()
    await bot.send_message(
            chat_id=user_id, 
            text="Укажите дату рождения в формате 06.08.1987")

@codeRouter.message(DateFilter(is_date=True), FSMCode.calculate_code, flags=flags)
async def sending_result(message: Message) -> None:
    if message.text == None:
        return 
    result: str = await calculate_code(message.text)
    await message.answer(result)

@codeRouter.message(FSMCode.calculate_code, flags=flags)
async def wrong_input(message: Message) -> None:
    if message.text == None:
        return
    await message.reply("Не правильный формат даты")

