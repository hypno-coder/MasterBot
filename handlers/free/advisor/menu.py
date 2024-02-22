from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config_data import SpamConfig
from keyboards import Keyboard, advisor_menu_buttons
from lexicon import (AdvisorPagiBtnCallback, FreeMenuButtons,
                     advisor_description)

advisorMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.advisor_menu.name}


@advisorMenuRouter.callback_query(F.data == FreeMenuButtons.Advisor.name, flags=flags)
async def advisor_menu(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message == None:
        return

    page = 1
    await state.set_data(data={"page": page})
    text = advisor_description[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=Keyboard.create_pagi(
            AdvisorPagiBtnCallback.backward,
            f"{page}/{len(advisor_description)}",
            AdvisorPagiBtnCallback.forward,
            keyboard=advisor_menu_buttons,
        ),
    )

    await callback.answer()


@advisorMenuRouter.callback_query(F.data == AdvisorPagiBtnCallback.forward)
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return

    data = await state.get_data()

    try:
        if data["page"] == len(advisor_description):
            await callback.answer()
            return
    except Exception:
        data.update({"page": 1})

    page = data["page"] + 1
    await state.update_data(page=page)
    text = advisor_description[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=Keyboard.create_pagi(
            AdvisorPagiBtnCallback.backward,
            f"{page}/{len(advisor_description)}",
            AdvisorPagiBtnCallback.forward,
            keyboard=advisor_menu_buttons,
        ),
    )
    await callback.answer()


@advisorMenuRouter.callback_query(F.data == AdvisorPagiBtnCallback.backward)
async def process_backward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return
    data = await state.get_data()
    if data["page"] == 1:
        await callback.answer()
        return

    page = data["page"] - 1
    await state.update_data(page=page)
    text = advisor_description[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=Keyboard.create_pagi(
            AdvisorPagiBtnCallback.backward,
            f"{page}/{len(advisor_description)}",
            AdvisorPagiBtnCallback.forward,
            keyboard=advisor_menu_buttons,
        ),
    )
    await callback.answer()
