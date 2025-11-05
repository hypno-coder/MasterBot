import asyncio
import random
from decimal import Decimal
from typing import cast

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config_data import SpamConfig
from filters import AgeFilter, DateFilter, DayFilter
from keyboards import code_action_menu_keyboard, get_payment_keyboard, create_common_keyboard
from lexicon import (AdminPaidButtons, CodeActionMenuButtons, CodeLexicon,
                     CodeMenuButtons, CommonLexicon, PaidMenuButtons, ActionChoosePaymentButtons)
from loader import config, payment as PaymentCredentials
from payment_services import generate_payment_link, ProdamusClient
from payment_services.user_data_type import user_data
from services import ResponseController
from states import FSMCode
from utils import remove_message

codeHandlerRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.code_menu.name}


@codeHandlerRouter.callback_query(
    F.data.in_(
        [
            AdminPaidButtons.AdminMoneyCode.name,
            CodeMenuButtons.CalculateMoneyCode.name,
            CodeActionMenuButtons.CodeEditData.name,
        ]
    ),
    DayFilter(is_day=True),
    flags=flags,
)
async def enter_full_name(callback: CallbackQuery, state: FSMContext) -> None:
    admin_access = None
    message = cast(CallbackQuery, callback.message)

    if callback.data == AdminPaidButtons.AdminMoneyCode.name:
        admin_access = AdminPaidButtons.AdminMoneyCode.name
        await message.answer(text="Доступ Администратора")

    await state.set_data({"adminCallback": admin_access})

    await message.answer(text=CommonLexicon.enter_fio)
    await state.set_state(FSMCode.enter_date)


@codeHandlerRouter.callback_query(
    F.data.in_(
        [
            AdminPaidButtons.AdminMoneyCode.name,
            CodeMenuButtons.CalculateMoneyCode.name,
            CodeActionMenuButtons.CodeEditData.name,
        ]
    ),
    flags=flags,
)
async def day_except(callback: CallbackQuery, bot: Bot) -> None:
    if callback.message == None:
        return
    callback.answer()

    data = await bot.send_message(
        chat_id=callback.message.chat.id, text=CodeLexicon.only_thursday
    )
    asyncio.create_task(
        remove_message(chat_id=data.chat.id, message_id=data.message_id, delay=5)
    )


@codeHandlerRouter.message(FSMCode.enter_date, flags=flags)
async def enter_date(message: Message, state: FSMContext) -> None:
    if message.text == None or message.from_user == None:
        return

    fio: str = message.text
    data = await state.get_data()
    data.update({"fio": fio})
    await state.update_data(data)

    await message.answer(text=CommonLexicon.enter_date)
    await state.set_state(FSMCode.check_data)


@codeHandlerRouter.message(
    FSMCode.check_data,
    DateFilter(is_date=True),
    AgeFilter(is_age=True),
    flags=flags,
)
async def check_data(message: Message, state: FSMContext) -> None:
    if message.text == None or message.from_user == None:
        return

    data = await state.get_data()
    fio: str = data["fio"]
    birthday: str = message.text
    data.update({"birthday": birthday})
    await state.update_data(data)

    await message.answer(text=CommonLexicon.check_data)
    await message.answer(text=f"{CommonLexicon.fio}{fio}")
    await message.answer(text=f"{CommonLexicon.birthday}{birthday}")
    await message.answer(
        text=CommonLexicon.selected_action, reply_markup=code_action_menu_keyboard
    )


@codeHandlerRouter.message(FSMCode.check_data, DateFilter(is_date=True), flags=flags)
async def wrong_age(message: Message) -> None:
    if message.text == None:
        return
    await message.reply(CommonLexicon.legal_age)


@codeHandlerRouter.message(FSMCode.check_data, flags=flags)
async def wrong_input(message: Message) -> None:
    if message.text == None:
        return
    await message.reply(CommonLexicon.invalid_format_date)

    
@codeHandlerRouter.callback_query(
    F.data == CodeActionMenuButtons.CodeConfirmData.name,
    flags=flags,
)
async def choosing_payment_method(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.message == None:
        return
    callback.answer()
    
    await callback.message.answer(
        text=CommonLexicon.choose_payment_method,
        reply_markup=create_common_keyboard(
            ActionChoosePaymentButtons,
        )
    )
    await state.set_state(FSMCode.successful_payment)


@codeHandlerRouter.callback_query(
    FSMCode.successful_payment,
    F.data.in_(
        [
            ActionChoosePaymentButtons.payment_in_russia.name,
            ActionChoosePaymentButtons.payment_other_countries.name,
        ]
    ),
)
async def order(callback: CallbackQuery, state: FSMContext):
    callback.answer()
    message = callback.message
    data: dict = await state.get_data()

    if message == None or message.from_user == None:
        return

    user_data["chat_id"] = message.chat.id
    user_data["user_id"] = message.from_user.id
    user_data["service_species"] = PaidMenuButtons.MoneyCode.name
    user_data["fio"] = data["fio"]
    user_data["birthday"] = data["birthday"]
    user_data["adminCallback"] = data["adminCallback"]
    user_data["min_delay"] = "180"
    user_data["max_delay"] = "360"

    if data["adminCallback"] != None and F.from_user.id.in_(config.tg_bot.admin_ids):
        user_data["min_delay"] = "1"
        user_data["max_delay"] = "2"
        response = ResponseController(user_data=user_data)
        await response.launch()
        await state.clear()
        return
    
    if callback.data == ActionChoosePaymentButtons.payment_in_russia.name:
        link = generate_payment_link(
            cost=Decimal(f"{PaymentCredentials.price.money_code}.00"),
            number=random.randint(10**6, (10**7) - 1),
            user_data=user_data,
            description=f"Консультация: {PaidMenuButtons.MoneyCode.value}",
        )

        
    if callback.data == ActionChoosePaymentButtons.payment_other_countries.name:
        prodamus = ProdamusClient("link")
        link = prodamus.generate_link(
            price=str(PaymentCredentials.price.money_code),
            order_id=str(random.randint(10**6, (10**7) - 1)),
            name=PaidMenuButtons.MoneyCode.value,
            user_data=user_data

        )

    await message.answer(
        text=CommonLexicon.pay_message,
        reply_markup=get_payment_keyboard(
            link=link, backbutton=PaidMenuButtons.BackToPaidMenu
        ),
    )
        
    await state.clear()
