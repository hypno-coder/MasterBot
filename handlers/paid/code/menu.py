from aiogram import Router
from aiogram.types import CallbackQuery 
from aiogram.filters import Text 
from aiogram.fsm.context import FSMContext 

from keyboards import create_pagination_keyboard, code_menu_keyboard, BotCBData
from lexicon import code_text
from config_data import SpamConfig

codeMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.code_menu.name}

@codeMenuRouter.callback_query(
        lambda a: a.data == BotCBData.MoneyCodeBtn1.value, 
        flags=flags)
async def code_menu(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message == None:
        return

    page = 1
    await state.set_data(data={"page": page})
    text = code_text[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
                    'code_backward',
                    f'{page}/{len(code_text)}',
                    'code_forward',
                    keyboard=code_menu_keyboard ))
        
    await callback.answer()


@codeMenuRouter.callback_query(Text(text='code_forward'))
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return

    data = await state.get_data()
    if data['page'] == len(code_text):
        await callback.answer()
        return

    page = data['page'] + 1
    await state.update_data(page=page)
    text = code_text[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
                'code_backward',
                f'{page}/{len(code_text)}',
                'code_forward',
                keyboard=code_menu_keyboard ))
    await callback.answer()

@codeMenuRouter.callback_query(Text(text='code_backward'))
async def process_backward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return

    data = await state.get_data()
    if data['page'] == 1:
        await callback.answer()
        return

    page = data['page'] - 1
    await state.update_data(page=page)
    text = code_text[page]

    await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'code_backward',
                f'{page}/{len(code_text)}',
                'code_forward',
                keyboard=code_menu_keyboard ))
    await callback.answer()
