from typing import cast

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery 
from aiogram.fsm.context import FSMContext

from keyboards import mailing_action_menu_keyboard, mailing_button_menu_keyboard 
from lexicon import MailingLexicon, AdminMenuButtons, MailingActionMenuButtons, MailingButtonMenu, CommonLexicon 
from config_data import SpamConfig
from states import FSMMailing
from services import Sender

mailingHandlerRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.mailing_menu.name}


@mailingHandlerRouter.callback_query(
        F.data.in_([AdminMenuButtons.Mailing.name, 
                    MailingActionMenuButtons.MailingEditData.name]), flags=flags)
async def enter_company_name(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=MailingLexicon.enter_company_name) 
    await state.clear()
    await state.set_state(FSMMailing.enter_message)


@mailingHandlerRouter.message(~F.text.startswith('/'), FSMMailing.enter_message, flags=flags)
async def enter_message(message: Message, state: FSMContext) -> None:
    if message.text == None or message.from_user == None:
        return

    mailing_name: str = message.text 
    await state.set_data({'mailing_name': mailing_name})

    await message.answer(text=MailingLexicon.enter_message)
    await state.set_state(FSMMailing.enter_image)


@mailingHandlerRouter.message(~F.text.startswith('/'), FSMMailing.enter_image, flags=flags)
async def enter_image(message: Message, state: FSMContext) -> None:
    if message.text == None or message.from_user == None:
        return

    mailing_message: str = message.text 
    data = await state.get_data() 
    data.update({'mailing_message': mailing_message})
    await state.update_data(data)

    await message.answer(text=MailingLexicon.enter_image)
    await state.set_state(FSMMailing.add_button)


@mailingHandlerRouter.message(F.text == '0', FSMMailing.add_button, flags=flags)
@mailingHandlerRouter.message(F.photo, FSMMailing.add_button, flags=flags)
async def push_button_menu(message: Message, state: FSMContext) -> None:
    data = await state.get_data() 

    if message.photo != None:
        photo = message.photo[-1]
        photo_id: str = photo.file_id
        data.update({'photo_id': photo_id})
        await state.update_data(data)

    if message.text != None:
        data.update({'photo_id': '0'})
        await state.update_data(data)

    await message.answer(text=MailingLexicon.button_menu, reply_markup=mailing_button_menu_keyboard)


@mailingHandlerRouter.callback_query(
        F.data == MailingButtonMenu.MailingAddButton.name, flags=flags)
async def add_button_name(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=MailingLexicon.button_name) 
    await state.set_state(FSMMailing.button_link)


@mailingHandlerRouter.message(~F.text.startswith('/'), FSMMailing.button_link, flags=flags)
async def add_button_link(message: Message, state: FSMContext) -> None:
    message = cast(Message, message)

    data = await state.get_data() 
    data.update({'button_name': message.text})
    await state.update_data(data)

    await message.answer(
            text=MailingLexicon.button_link) 
    await state.set_state(FSMMailing.check_data)


@mailingHandlerRouter.callback_query(
        F.data == MailingButtonMenu.MailingUnbutton.name, flags=flags)
@mailingHandlerRouter.message(~F.text.startswith('/'), FSMMailing.check_data, flags=flags)
async def check_data(event: Message | CallbackQuery, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data() 

    chat_id: int = 0 
    mailing_name: str = data['mailing_name']
    mailing_message: str = data['mailing_message']
    photo_id: str = data['photo_id']
    button_name: str | None = None
    button_link: str | None = None

    if isinstance(event, Message):
        chat_id = event.chat.id
        data.update({'button_link': event.text})
        await state.update_data(data)
        button_name = data['button_name']
        button_link = data['button_link']

    if isinstance(event, CallbackQuery) and event.message != None:
        chat_id = event.message.chat.id
        data.update({'button_name':button_name})
        data.update({'button_link':button_link})
        await state.update_data(data)
        event.answer()
 
    await bot.send_message(chat_id, text=CommonLexicon.check_data)
    await bot.send_message(chat_id, text=f'{MailingLexicon.company_name} {mailing_name}')
    await bot.send_message(chat_id, text=f'{MailingLexicon.message_for_mailing} n/ {mailing_message}')

    if photo_id == '0':
        await bot.send_message(chat_id, text=MailingLexicon.unimage)
    else:
        await bot.send_photo(chat_id, photo_id)

    if button_name != None and button_link != None:
        await bot.send_message(chat_id, text=f'{MailingLexicon.button_name} {button_name}')
        await bot.send_message(chat_id, text=f'{MailingLexicon.button_link} {button_link}')
    else: 
        await bot.send_message(chat_id, text=MailingLexicon.unbutton)

    await bot.send_message(chat_id, text=CommonLexicon.selected_action, reply_markup=mailing_action_menu_keyboard)

@mailingHandlerRouter.callback_query(
        F.data == MailingActionMenuButtons.StartMailing.name, flags=flags)
async def start_mailing(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data() 
    sender = Sender(bot, data)
    await sender.start()
    callback.answer(text=MailingLexicon.mailing_is_complete)
