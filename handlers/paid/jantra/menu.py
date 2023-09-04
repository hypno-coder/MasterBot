from aiogram import Router
from aiogram.types import CallbackQuery 
from aiogram.filters import Text 
from aiogram.fsm.context import FSMContext 

from keyboards import create_pagination_keyboard,jantra_menu_keyboard,  BotCBData
from lexicon import jantra_text
from config_data import SpamConfig

jantraMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.jantra_menu.name}

@jantraMenuRouter.callback_query(lambda a: a.data == BotCBData.JantraBtn1.value, flags=flags)
async def jantra_menu(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message == None:
        return
    
    page = 1
    await state.set_data(data={'page': page})
    text = jantra_text[page]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
                    'jantra_backward',
                    f'{page}/{len(jantra_text)}',
                    'jantra_forward',
                    keyboard=jantra_menu_keyboard ))
    await callback.answer()


@jantraMenuRouter.callback_query(Text(text='jantra_forward'))
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
                'jantra_backward',
                f'{page}/{len(jantra_text)}',
                'jantra_forward',
                keyboard=jantra_menu_keyboard ))

@jantraMenuRouter.callback_query(Text(text='jantra_backward'))
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
                'jantra_backward',
                f'{page}/{len(jantra_text)}',
                'jantra_forward',
                keyboard=jantra_menu_keyboard ))
