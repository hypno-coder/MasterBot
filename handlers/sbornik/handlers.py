import base64
import random
from decimal import Decimal
from typing import cast

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config_data import SpamConfig
from filters import AgeFilter, DateFilter
from keyboards import get_payment_keyboard, jantra_action_menu_keyboard
from lexicon import (AdminPaidButtons, CommonLexicon, JantraActionMenuButtons,
                     JantraMenuButtons, MainMenuButtons, PaidMenuButtons)
from loader import config
from loader import payment as PaymentCredentials
from payment_services import generate_payment_link
from payment_services.user_data_type import user_data
from services import Jantra, ResponseController
from states import FSMJantra

sbornikHandlerRouter: Router = Router()


@sbornikHandlerRouter.callback_query(
    F.data.in_(
        [
            AdminPaidButtons.AdminMoenyCollection.name,
            MainMenuButtons.MoenyCollection.name,
        ]
    )
)
async def order(callback: CallbackQuery, state: FSMContext):
    admin_access = None
    assert callback.message
    assert callback.message.from_user
    assert callback.message.chat.username

    if callback.data == AdminPaidButtons.AdminMoenyCollection.name:
        admin_access = AdminPaidButtons.AdminMoenyCollection.name

    user_data["chat_id"] = callback.message.chat.id
    user_data["user_id"] = callback.message.from_user.id
    user_data["fio"] = callback.message.chat.first_name or callback.message.chat.username
    user_data["service_species"] = MainMenuButtons.MoenyCollection.name
    user_data["adminCallback"] = admin_access
    user_data["min_delay"] = "0"
    user_data["max_delay"] = "0"

    if admin_access != None and F.from_user.id.in_(config.tg_bot.admin_ids):
        user_data["min_delay"] = "1"
        user_data["max_delay"] = "2"
        response = ResponseController(user_data=user_data)
        await response.launch()
        await state.clear()
        return

    link = generate_payment_link(
        cost=Decimal(f"990.00"),
        number=random.randint(10**6, (10**7) - 1),
        user_data=user_data,
        description=f"Курс: {MainMenuButtons.MoenyCollection.value}",
    )

    await callback.message.answer(
        text=CommonLexicon.pay_message,
        reply_markup=get_payment_keyboard(
            link=link, backbutton=PaidMenuButtons.BackToPaidMenu
        ),
    )
