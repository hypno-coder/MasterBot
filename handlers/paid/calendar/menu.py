from aiogram import Router, F
from aiogram.types import CallbackQuery 
from aiogram.fsm.context import FSMContext 

from keyboards import create_pagination_keyboard, calendar_menu_keyboard 
from lexicon import calendar_description, PaidMenuButtons 
from config_data import SpamConfig

calendarMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.calendar_menu.name}


@calendarMenuRouter.callback_query(F.data == PaidMenuButtons.MoneyCalendar.name, flags=flags)
async def calendar_menu(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message == None:
        return

    page = 1
    await state.set_data(data={"page": page})
    text = calendar_description[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
                    'calendar_backward',
                    f'{page}/{len(calendar_description)}',
                    'calendar_forward',
                    keyboard=calendar_menu_keyboard ))
        
    await callback.answer()


@calendarMenuRouter.callback_query(F.data == 'calendar_forward')
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return

    data = await state.get_data()
    if data['page'] == len(calendar_description):
        await callback.answer()
        return

    page = data['page'] + 1
    await state.update_data(page=page)
    text = calendar_description[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
                'calendar_backward',
                f'{page}/{len(calendar_description)}',
                'calendar_forward',
                keyboard=calendar_menu_keyboard ))
    await callback.answer()

@calendarMenuRouter.callback_query(F.data == 'calendar_backward')
async def process_backward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return
    data = await state.get_data()
    if data['page'] == 1:
        await callback.answer()
        return

    page = data['page'] - 1
    await state.update_data(page=page)
    text = calendar_description[page]

    await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'calendar_backward',
                f'{page}/{len(calendar_description)}',
                'calendar_forward',
                keyboard=calendar_menu_keyboard ))
    await callback.answer()
