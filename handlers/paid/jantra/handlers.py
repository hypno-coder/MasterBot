from typing import cast
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile 

from loader import payment
from keyboards import BotCBData
from lexicon import BotText 
from config_data import SpamConfig
from states import FSMJantra
from filters import DateFilter, AgeFilter
from services import Jantra 
from utils import send_message_with_delay

jantraHandlerRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.code_menu.name}

@jantraHandlerRouter.callback_query(
        lambda a: a.data == BotCBData.JantraBtn2.value, flags=flags)
async def eter_full_name(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=BotText.fio) 
    await state.set_state(FSMJantra.enter_date)

@jantraHandlerRouter.message(FSMJantra.enter_date, flags=flags)
async def enter_date(message: Message, state: FSMContext) -> None:
    await message.answer(
            text=BotText.money_code_date)
    await state.set_state(FSMJantra.payment)

@jantraHandlerRouter.message(DateFilter(is_date=True), AgeFilter(is_age=True), FSMJantra.payment, flags=flags)
async def order(message: Message, bot: Bot, state: FSMContext):
    if message.from_user == None:
        return

    user_id = message.from_user.id
    await state.set_data({f"date_{user_id}": message.text})
    await bot.send_invoice( 
                           chat_id=message.chat.id,
                           title=BotText.jantra_title,
                           description=BotText.jantra_payment_description,
                           payload=BotText.jantra_payload,
                           provider_token=payment.yoomoney.token,
                           currency=payment.currency,
                           prices=[
                               LabeledPrice(
                                   label=BotText.jantra_title,
                                   amount=int(str(payment.price.jantra) + '00'),
                                   )])
                               
    await state.set_state(FSMJantra.checkout_query)

@jantraHandlerRouter.message(DateFilter(is_date=True), FSMJantra.payment, flags=flags)
async def wrong_age(message: Message) -> None:
    if message.text == None:
        return

    await message.reply(BotText.legal_age)

@jantraHandlerRouter.message(FSMJantra.payment, flags=flags)
async def wrong_input(message: Message) -> None:
    if message.text == None:
        return

    await message.reply(BotText.invalid_format_date)

@jantraHandlerRouter.pre_checkout_query(FSMJantra.checkout_query, flags=flags)
async def pre_chechout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await state.set_state(FSMJantra.successful_payment)

@jantraHandlerRouter.message(
        F.content_type.in_(ContentType.SUCCESSFUL_PAYMENT), FSMJantra.successful_payment, flags=flags)
async def successful_payment(message: Message, state: FSMContext) -> None:
    if message.from_user == None:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id
    data = await state.get_data() 
    date: str = data[f"date_{user_id}"] 
    image, number = Jantra.create(date)
    input_image = BufferedInputFile(image, 'jantra.png')
    await send_message_with_delay(
            chat_id, 
            100, 200, 
            name=BotText.jantra_title,
            text=BotText.jantra_lucky_number+str(number), image=input_image)
