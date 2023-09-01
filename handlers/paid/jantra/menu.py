from aiogram import Router
from aiogram.types import CallbackQuery, Message 
from aiogram.filters import Text 
from aiogram.fsm.context import FSMContext 
from aiogram import html

from keyboards import create_pagination_keyboard, BotCBData
from lexicon import jantra_text
from utils import remove_message
from config_data import SpamConfig

jantraMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.jantra_menu.name}

@jantraMenuRouter.callback_query(lambda a: a.data == BotCBData.JantraBtn1.value, flags=flags)
async def jantra_menu(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message == None:
        return

    page = 1
    await state.set_data(data={"page": page})
    text = jantra_text[page]

    resp: Message | bool = await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{page}/{len(jantra_text)}',
                    'forward'))


@jantraMenuRouter.callback_query(Text(text='forward'))
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return

    data = await state.get_data()
    if data['page'] == len(jantra_text):
        await callback.answer()
        return

    page = data['page'] + 1
    await state.update_data(page=page)
    text = jantra_text[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
                'backward',
                f'{page}/{len(jantra_text)}',
                'forward'))
    await callback.answer()

@jantraMenuRouter.callback_query(Text(text='backward'))
async def process_backward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return

    data = await state.get_data()
    if data['page'] == 1:
        await callback.answer()
        return

    page = data['page'] - 1
    await state.update_data(page=page)
    text = jantra_text[page]

    await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{page}/{len(jantra_text)}',
                'forward'))
    await callback.answer()
