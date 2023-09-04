from aiogram import Router
from aiogram.types import CallbackQuery 
from aiogram.filters import Text 
from aiogram.fsm.context import FSMContext 

from keyboards import create_pagination_keyboard, calendar_menu_keyboard, BotCBData
from lexicon import calendar_text
from config_data import SpamConfig

calendarMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.calendar_menu.name}


@calendarMenuRouter.callback_query(
        lambda a: a.data == BotCBData.MoneyCalendarBtn1.value, 
        flags=flags)
async def calendar_menu(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message == None:
        return

    page = 1
    await state.set_data(data={"page": page})
    text = calendar_text[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
                    'calendar_backward',
                    f'{page}/{len(calendar_text)}',
                    'calendar_forward',
                    keyboard=calendar_menu_keyboard ))
        
    await callback.answer()


@calendarMenuRouter.callback_query(Text(text='calendar_forward'))
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return

    data = await state.get_data()
    if data['page'] == len(calendar_text):
        await callback.answer()
        return

    page = data['page'] + 1
    await state.update_data(page=page)
    text = calendar_text[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
                'calendar_backward',
                f'{page}/{len(calendar_text)}',
                'calendar_forward',
                keyboard=calendar_menu_keyboard ))
    await callback.answer()

@calendarMenuRouter.callback_query(Text(text='calendar_backward'))
async def process_backward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return
    data = await state.get_data()
    if data['page'] == 1:
        await callback.answer()
        return

    page = data['page'] - 1
    await state.update_data(page=page)
    text = calendar_text[page]

    await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'calendar_backward',
                f'{page}/{len(calendar_text)}',
                'calendar_forward',
                keyboard=calendar_menu_keyboard ))
    await callback.answer()
