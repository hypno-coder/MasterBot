import re
from aiogram import Router
from aiogram import Bot 
from aiogram.types import CallbackQuery, Message 
from aiogram.fsm.context import FSMContext

from keyboards import BotCBData 
from lexicon import BotText 
from config_data import SpamConfig
from services import Sonnik, SonnikTypeArticle, SonnikTypeResponse 
from keyboards import sonnik_repeat_keyboard
from errors import send_error_message
from states import FSMSonnik

sonnikRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.sonnik_conv.name}

@sonnikRouter.callback_query(lambda a: a.data == BotCBData.Btn2.value, flags=flags)
async def start_sonnik_conv(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    if callback.message == None:
        return
    await callback.message.delete()
    await state.set_state(FSMSonnik.enter_image)
    user_id = callback.from_user.id
    await callback.answer()
    await bot.send_message(chat_id=user_id, text=BotText.sonnik_conv['start'])

@sonnikRouter.message(lambda a: bool(re.match(r'^[А-Яа-я]+$', a.text)) ,FSMSonnik.enter_image)
async def process_name(message: Message, state: FSMContext) -> None:

    # await message.delete()
    await message.answer(text='Ожидайте, идет проработка...')
    await state.clear()
    sonnik = Sonnik()
    if message.text == None:
        return
    text_image: str = message.text
    response: SonnikTypeResponse = sonnik.interpret(text_image.strip())
    error: str | None = response["error"]
    data: list[SonnikTypeArticle] = response["data"]
    await message.delete()

    if error != None:
        await send_error_message(error)
        await message.answer(text='Сонник пока не работает, попробуйте позже')
        return

    for chapter in data:
        await message.answer(text=f"{chapter['title']} \n\n {chapter['text']}")

    await message.answer(text="Попробовать другой образ сна :", reply_markup=sonnik_repeat_keyboard)



@sonnikRouter.message(FSMSonnik.enter_image)
async def text_filter(message: Message):
    await message.answer(
            text='Нужно писать в сooбщении только ОДНО' 
            'слово кирилицей без каких либо других символов или цифр')



