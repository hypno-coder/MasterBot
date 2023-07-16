from aiogram import Router
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Text
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboards import main_menu_keyboard, BotCBData 
from lexicon import BotText, BotBtnText
from config_data import SpamConfig
from services import Sonnik, SonnikTypeArticle, SonnikTypeResponse 
from errors import send_error_message
from states import FSMSonnik

router: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.sonnik_conv.name}

@router.callback_query(lambda a: a.data == BotCBData.Btn2.value, flags=flags)
async def start_sonnik_conv(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await state.set_state(FSMSonnik.enter_image)
    user_id = callback.from_user.id
    await callback.answer()
    await bot.send_message(chat_id=user_id, text=BotText.sonnik_conv['start'])

@router.message(FSMSonnik.enter_image)
async def process_name(message: Message, state: FSMContext) -> None:
    await message.answer(text='Ожидайте, идет проработка...')
    await state.clear()
    sonnik = Sonnik()
    if message.text == None:
        return
    text_image: str = message.text
    response: SonnikTypeResponse = sonnik.interpret(text_image)
    error_status: bool = response["error"]
    if error_status:
        await send_error_message('упал парсинг сонника')
        await message.answer(text='Сонник пока не работает, попробуйте позже')
    data: list[SonnikTypeArticle] = response["data"]
    for chapter in data:
        await message.answer(text=chapter['text'])


