from typing import cast
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from keyboards import code_menu_keyboard 
from loader import payment
from staticfiles import FilePath
from keyboards import BotCBData
from lexicon import BotText 
from config_data import SpamConfig
from states import FSMCode
from filters import DateFilter, DayFilter, AgeFilter
from services import calculate_code
from utils import send_message_with_delay

codeHandlerRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.code_menu.name}

@codeHandlerRouter.callback_query(lambda a: a.data == BotCBData.MoneyCodeBtn1.value, flags=flags)
async def start_code_conversation(callback: CallbackQuery, state: FSMContext):
    if callback.message == None:
        return
    await callback.message.edit_text(text=BotText.money_code_description, reply_markup=code_menu_keyboard)
    await state.set_state(FSMCode.enter_full_name)

@codeHandlerRouter.callback_query(lambda a: a.data == BotCBData.MoneyCodeBtn2.value, FSMCode.enter_full_name, DayFilter(is_day=True), flags=flags)
async def enter_full_name(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=BotText.fio) 
    await state.set_state(FSMCode.enter_date)
@codeHandlerRouter.callback_query(lambda a: a.data == BotCBData.MoneyCodeBtn2.value, flags=flags)
async def day_except(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=BotText.money_code_only_thursday)
    await state.clear()

@codeHandlerRouter.message(FSMCode.enter_date, flags=flags)
async def enter_date(message: Message, state: FSMContext) -> None:
    await message.answer(
            text=BotText.money_code_date)
    await state.set_state(FSMCode.payment)

@codeHandlerRouter.message(DateFilter(is_date=True), AgeFilter(is_age=True), FSMCode.payment, flags=flags)
async def order(message: Message, bot: Bot, state: FSMContext):
    await state.set_data({"date": message.text})
    await bot.send_invoice( 
                           chat_id=message.chat.id,
                           title=BotText.money_code_title,
                           description=BotText.money_code_payment_description,
                           payload=BotText.money_code_payload,
                           provider_token=payment.yoomoney.token,
                           currency=payment.currency,
                           prices=[
                               LabeledPrice(
                                   label=BotText.money_code_title,
                                   amount=int(str(payment.price.money_code) + '00'),
                                   )])
                               
    await state.set_state(FSMCode.checkout_query)

@codeHandlerRouter.message(DateFilter(is_date=True), FSMCode.payment, flags=flags)
async def wrong_age(message: Message) -> None:
    if message.text == None:
        return

    await message.reply(BotText.legal_age)

@codeHandlerRouter.message(FSMCode.payment, flags=flags)
async def wrong_input(message: Message) -> None:
    if message.text == None:
        return
    await message.reply(BotText.invalid_format_date)

@codeHandlerRouter.pre_checkout_query(FSMCode.checkout_query, flags=flags)
async def pre_chechout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await state.set_state(FSMCode.successful_payment)

@codeHandlerRouter.message(
        F.content_type.in_(ContentType.SUCCESSFUL_PAYMENT), FSMCode.successful_payment, flags=flags)
async def successful_payment(message: Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    data = await state.get_data() 
    result: str = await calculate_code(data['date']) 
    document = FSInputFile(FilePath.money_code_pdf.value)
    video = FSInputFile(FilePath.money_code_video.value)
    await state.clear()
    await send_message_with_delay(
            chat_id, 
            100, 200, 
            text=BotText.money_code_for_you+result,
            video=video, 
            document=document, 
            document_caption=BotText.money_code_document)
