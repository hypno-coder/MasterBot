from typing import cast
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext

from keyboards import calendar_menu_keyboard 
from loader import payment
from keyboards import BotCBData
from lexicon import BotText 
from config_data import SpamConfig
from states import FSMCalendar
from services import get_calendar_dates 
from utils import send_message_with_delay

calendarHandlerRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.calendar_menu.name}

@calendarHandlerRouter.callback_query(lambda a: a.data == BotCBData.MoneyCalendarBtn1.value, flags=flags)
async def start_calendar_conversation(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return
    await callback.message.edit_text(
            text=BotText.money_calendar_description, 
            reply_markup=calendar_menu_keyboard)
    await state.set_state(FSMCalendar.enter_full_name)

@calendarHandlerRouter.callback_query(
        lambda a: a.data == BotCBData.MoneyCalendarBtn2.value, 
        FSMCalendar.enter_full_name, flags=flags)
async def enter_full_name(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=BotText.fio)
    await state.set_state(FSMCalendar.enter_date)

@calendarHandlerRouter.message(FSMCalendar.enter_date, flags=flags)
async def enter_date(message: Message, state: FSMContext) -> None:
    await message.answer(
            text=BotText.money_code_date)
    await state.set_state(FSMCalendar.payment)

@calendarHandlerRouter.message(FSMCalendar.payment, flags=flags)
async def order(message: Message, bot: Bot, state: FSMContext):
    await bot.send_invoice( 
                           chat_id=message.chat.id,
                           title=BotText.money_calendar_title,
                           description=BotText.money_calendar_payment_description,
                           payload=BotText.money_calendar_payload,
                           provider_token=payment.yoomoney.token,
                           currency=payment.currency,
                           prices=[
                               LabeledPrice(
                                   label=BotText.money_calendar_title,
                                   amount=int(str(payment.price.money_calendar) + '00'),
                                   )])
                               
    await state.set_state(FSMCalendar.checkout_query)

@calendarHandlerRouter.pre_checkout_query(FSMCalendar.checkout_query, flags=flags)
async def pre_chechout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await state.set_state(FSMCalendar.successful_payment)

@calendarHandlerRouter.message(
        F.content_type.in_(ContentType.SUCCESSFUL_PAYMENT), FSMCalendar.successful_payment, flags=flags)
async def successful_payment(message: Message, state: FSMContext) -> None:
    await state.clear()
    chat_id = message.chat.id
    numbers = get_calendar_dates()
    result = ''.join(str(num) for num in numbers)
    await send_message_with_delay(chat_id, 100, 200, text=BotText.money_calendar_for_you + result)
