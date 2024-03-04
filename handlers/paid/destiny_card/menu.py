from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config_data import SpamConfig
from keyboards import Keyboard, destiny_card_menu_buttons
from lexicon import (DestinyCardPagiBtnCallback, PaidMenuButtons,
                     destiny_card_description)

destinyCardMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.destiny_card_menu.name}


@destinyCardMenuRouter.callback_query(
    F.data == PaidMenuButtons.DestinyCard.name, flags=flags
)
async def destiny_card_menu(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message == None:
        return

    page = 1
    await state.set_data(data={"page": page})
    text = destiny_card_description[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=Keyboard.create_pagi(
            DestinyCardPagiBtnCallback.backward,
            f"{page}/{len(destiny_card_description)}",
            DestinyCardPagiBtnCallback.forward,
            keyboard=destiny_card_menu_buttons,
        ),
    )

    await callback.answer()


@destinyCardMenuRouter.callback_query(F.data == DestinyCardPagiBtnCallback.forward)
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return

    data = await state.get_data()
    try:
        if data["page"] == len(destiny_card_description):
            await callback.answer()
            return
    except Exception:
        data.update({"page": 1})

    page = data["page"] + 1
    await state.update_data(page=page)
    text = destiny_card_description[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=Keyboard.create_pagi(
            DestinyCardPagiBtnCallback.backward,
            f"{page}/{len(destiny_card_description)}",
            DestinyCardPagiBtnCallback.forward,
            keyboard=destiny_card_menu_buttons,
        ),
    )
    await callback.answer()


@destinyCardMenuRouter.callback_query(F.data == DestinyCardPagiBtnCallback.backward)
async def process_backward_press(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return

    data = await state.get_data()
    if data["page"] == 1:
        await callback.answer()
        return

    page = data["page"] - 1
    await state.update_data(page=page)
    text = destiny_card_description[page]

    await callback.message.edit_text(
        text=text,
        reply_markup=Keyboard.create_pagi(
            DestinyCardPagiBtnCallback.backward,
            f"{page}/{len(destiny_card_description)}",
            DestinyCardPagiBtnCallback.forward,
            keyboard=destiny_card_menu_buttons,
        ),
    )
    await callback.answer()
