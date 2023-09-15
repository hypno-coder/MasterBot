import re
from aiogram import Router
from aiogram import Bot 
from aiogram.types import CallbackQuery, Message 
from aiogram.fsm.context import FSMContext

from lexicon import BotText 
from config_data import SpamConfig
from services import SonnikTypeArticle, SonnikTypeResponse, Sonnik
from states import FSMSonnik
from keyboards import sonnik_repeat_keyboard
from errors import send_error_message
from utils import remove_message

sonnikRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.sonnik_conv.name}

@sonnikRouter.callback_query(lambda a: a.data == 'Sonnik', flags=flags)
async def start_sonnik_conv(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    if callback.message == None:
        return
    await callback.message.delete()
    await state.set_state(FSMSonnik.enter_image)
    user_id = callback.from_user.id
    await callback.answer()
    sent_message = await bot.send_message(chat_id=user_id, text=BotText.sonnik_conv['start'])
    await state.set_data(
            {'sonnik_message_id':f'{sent_message.message_id}',
             'sonnik_chat_id': f'{sent_message.chat.id}'})


@sonnikRouter.message(lambda a: bool(re.match(r'^[А-Яа-я]+$', a.text)) ,FSMSonnik.enter_image)
async def process_image(message: Message, bot: Bot, state: FSMContext) -> None:

    context = await state.get_data()
    chat_id = context['sonnik_chat_id']
    message_id = context['sonnik_message_id']
    await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, 
            text=BotText.sonnik_download_message)

    await state.clear()
    if message.text == None:
        return

    text_image: str = message.text
    sonnik: Sonnik = Sonnik()
    response: SonnikTypeResponse = sonnik.interpret(text_image.strip())
    error: str | None = response["error"]
    data: list[SonnikTypeArticle] = response["data"]

    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    if error != None:
        await send_error_message(error)
        await message.answer(text=BotText.sonnik_error_message)
        return

    for chapter in data:
        await message.answer(text=f"__{chapter['title']}__ \n\n {chapter['text']}")

    await message.answer(text=BotText.sonnik_try_another_image, reply_markup=sonnik_repeat_keyboard)



@sonnikRouter.message(FSMSonnik.enter_image)
async def text_filter(message: Message, bot: Bot):
    id = message.chat.id
    await message.delete()
    data = await bot.send_message(
            chat_id=id,
            text=f"{message.text} {BotText.sonnik_wrong_message}")
    await remove_message(chat_id=data.chat.id, message_id=data.message_id, delay=10)
    

