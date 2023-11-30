import re

from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message 
from aiogram.fsm.context import FSMContext

from lexicon import SonnikMenuButtons, CommonLexicon, SonnikActionMenuButtons, SonnikLexicon 
from config_data import SpamConfig
from services import Sonnik
from states import FSMSonnik
from keyboards import sonnik_repeat_keyboard
from utils import remove_message

sonnikHandlerRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.sonnik_conv.name}

@sonnikHandlerRouter.callback_query(F.data == SonnikMenuButtons.GetSonnik.name, flags=flags)
@sonnikHandlerRouter.callback_query(F.data == SonnikActionMenuButtons.Repeat.name, flags=flags)
async def start_sonnik_conv(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    if callback.message == None:
        return
    await callback.message.delete()
    await state.set_state(FSMSonnik.sleeping_pattern)
    user_id = callback.from_user.id
    await callback.answer()
    sent_message = await bot.send_message(chat_id=user_id, text=SonnikLexicon.conv)
    await state.set_data(
            {'sonnik_message_id':f'{sent_message.message_id}',
             'sonnik_chat_id': f'{sent_message.chat.id}'})


@sonnikHandlerRouter.message(lambda a: bool(re.match(r'^[А-Яа-я]+$', a.text)) ,FSMSonnik.sleeping_pattern)
async def process_image(message: Message, bot: Bot, state: FSMContext) -> None:

    chat_id = message.chat.id
    context = await state.get_data()
    chat_id = context['sonnik_chat_id']
    message_id = context['sonnik_message_id']
    await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, 
            text=SonnikLexicon.download_message)

    await state.clear()
    if message.text == None:
        return

    text_image: str = message.text.strip().lower()
    sonnik: Sonnik = Sonnik(text_image)
    articles = await sonnik.get()

    if articles == None: 
        await bot.send_message(
                chat_id=chat_id,
                text=SonnikLexicon.nothing_found,
                reply_markup=sonnik_repeat_keyboard)
        return

    for article in articles:
        await bot.send_message(
            chat_id=chat_id,
            text=article['header'])
        await bot.send_message(
            chat_id=chat_id,
            text=article['paragraph'])
        await bot.send_message(
            chat_id=chat_id,
            text=CommonLexicon.divider)

    await bot.send_message(
            chat_id=chat_id,
            text=SonnikLexicon.change_action, 
            reply_markup=sonnik_repeat_keyboard)


@sonnikHandlerRouter.message(FSMSonnik.sleeping_pattern)
async def text_filter(message: Message, bot: Bot):
    id = message.chat.id
    await message.delete()
    data = await bot.send_message(
            chat_id=id,
            text=f"{message.text} {SonnikLexicon.wrong_message}")
    await remove_message(chat_id=data.chat.id, message_id=data.message_id, delay=10)
