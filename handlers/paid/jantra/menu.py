from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config_data import SpamConfig
from keyboards import Keyboard, jantra_menu_buttons
from lexicon import JantraPagiBtnCallback, PaidMenuButtons, jantra_description

jantraMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.jantra_menu.name}


@jantraMenuRouter.callback_query(F.data == PaidMenuButtons.Jantra.name, flags=flags)
async def jantra_menu(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message == None:
        return

    page = 1
    await state.set_data(data={"page": page})
    text = jantra_description[page]
    await callback.message.edit_text(
        text=text,
        reply_markup=Keyboard.create_pagi(
            JantraPagiBtnCallback.backward,
            f"{page}/{len(jantra_description)}",
            JantraPagiBtnCallback.forward,
            keyboard=jantra_menu_buttons,
        ),
    )
    await callback.answer()


@jantraMenuRouter.callback_query(F.data == JantraPagiBtnCallback.forward)
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return

    data = await state.get_data()

    try:
        if data["page"] == len(jantra_description):
            await callback.answer()
            return
    except Exception:
        data.update({"page": 1})

    page = data["page"] + 1
    await state.update_data(page=page)
    text = jantra_description[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=Keyboard.create_pagi(
            JantraPagiBtnCallback.backward,
            f"{page}/{len(jantra_description)}",
            JantraPagiBtnCallback.forward,
            keyboard=jantra_menu_buttons,
        ),
    )


@jantraMenuRouter.callback_query(F.data == JantraPagiBtnCallback.backward)
async def process_backward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return

    data = await state.get_data()
    if data["page"] == 1:
        await callback.answer()
        return

    page = data["page"] - 1
    await state.update_data(page=page)
    text = jantra_description[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=Keyboard.create_pagi(
            JantraPagiBtnCallback.backward,
            f"{page}/{len(jantra_description)}",
            JantraPagiBtnCallback.forward,
            keyboard=jantra_menu_buttons,
        ),
    )
