from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config_data import SpamConfig
from keyboards import Keyboard, code_menu_buttons
from lexicon import CodePagiBtnCallback, PaidMenuButtons, code_description

codeMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.code_menu.name}


@codeMenuRouter.callback_query(F.data == PaidMenuButtons.MoneyCode.name, flags=flags)
async def code_menu(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message == None:
        return

    page = 1
    await state.set_data(data={"page": page})
    text = code_description[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=Keyboard.create_pagi(
            CodePagiBtnCallback.backward,
            f"{page}/{len(code_description)}",
            CodePagiBtnCallback.forward,
            keyboard=code_menu_buttons,
        ),
    )

    await callback.answer()


@codeMenuRouter.callback_query(F.data == CodePagiBtnCallback.forward)
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return

    data = await state.get_data()
    try:
        if data["page"] == len(code_description):
            await callback.answer()
            return
    except Exception:
        data.update({"page": 1})

    page = data["page"] + 1
    await state.update_data(page=page)
    text = code_description[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=Keyboard.create_pagi(
            CodePagiBtnCallback.backward,
            f"{page}/{len(code_description)}",
            CodePagiBtnCallback.forward,
            keyboard=code_menu_buttons,
        ),
    )
    await callback.answer()


@codeMenuRouter.callback_query(F.data == CodePagiBtnCallback.backward)
async def process_backward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return

    data = await state.get_data()
    if data["page"] == 1:
        await callback.answer()
        return

    page = data["page"] - 1
    await state.update_data(page=page)
    text = code_description[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=Keyboard.create_pagi(
            CodePagiBtnCallback.backward,
            f"{page}/{len(code_description)}",
            CodePagiBtnCallback.forward,
            keyboard=code_menu_buttons,
        ),
    )
    await callback.answer()
