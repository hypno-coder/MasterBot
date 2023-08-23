from typing import cast
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
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
from filters import DateFilter, DayFilter
from services import calculate_code

codeRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.code_menu.name}

text = """
    Приветствую! Это бот Мастерская Желаний, 
    со временем здесь появится Сонник, Гороскоп, 
    Афирмации, Янтра. 
    А сейчас  здесь можно расчитать свой финкод. 
    Для это нажми кнопку "Расчитать Финкод".
"""

@codeRouter.message(CommandStart(), flags=flags)
async def start_code_conversation(message: Message, state: FSMContext):
    await message.answer(text=text, reply_markup=code_menu_keyboard)
    await state.set_state(FSMCode.enter_full_name)

@codeRouter.callback_query(lambda a: a.data == BotCBData.MoneyCodeBtn1.value, FSMCode.enter_full_name, DayFilter(is_day=True), flags=flags)
async def eter_full_name(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=BotText.fio_for_money_code)
    await state.set_state(FSMCode.enter_date)

@codeRouter.callback_query(lambda a: a.data == BotCBData.MoneyCodeBtn1.value, flags=flags)
async def day_except(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=BotText.only_thursday)
    await state.clear()

@codeRouter.message(FSMCode.enter_date, flags=flags)
async def eter_date(message: Message, state: FSMContext) -> None:
    await message.answer(
            text=BotText.date_for_money_code)
    await state.set_state(FSMCode.payment_code)

@codeRouter.message(DateFilter(is_date=True), FSMCode.payment_code, flags=flags)
async def order(message: Message, bot: Bot, state: FSMContext):
    await state.set_data({"date": message.text})
    await bot.send_invoice( 
                           chat_id=message.chat.id,
                           title=BotText.title_money_code,
                           description=BotText.description_money_code,
                           payload=BotText.payload_money_code,
                           provider_token=payment.yoomoney.token,
                           currency=payment.currency,
                           prices=[
                               LabeledPrice(
                                   label=BotText.title_money_code,
                                   amount=int(str(payment.price.money_code) + '00'),
                                   )])
                               
    await state.set_state(FSMCode.checkout_query_code)


@codeRouter.message(FSMCode.payment_code, flags=flags)
async def wrong_input(message: Message) -> None:
    if message.text == None:
        return
    await message.reply(BotText.invalid_format_date)

@codeRouter.pre_checkout_query(FSMCode.checkout_query_code, flags=flags)
async def pre_chechout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@codeRouter.message(F.content_type.in_(ContentType.SUCCESSFUL_PAYMENT), flags=flags)
async def successful_payment(message: Message, bot: Bot, state: FSMContext) -> None:
    chat_id = message.chat.id
    data = await state.get_data()
    result: str = await calculate_code(data['date'])
    await message.answer(BotText.your_code+result)
    document = FSInputFile(FilePath.money_code_pdf.value)
    video = FSInputFile(FilePath.money_code_video.value)
    await bot.send_document(chat_id, document)
    await bot.send_video(chat_id, video)
