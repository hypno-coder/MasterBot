import re
from typing import cast
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, LabeledPrice, PreCheckoutQuery, pre_checkout_query, ContentType
from aiogram.fsm.context import FSMContext

from keyboards import code_menu_keyboard 
from lexicon import BotText, BotBtnText
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

@codeRouter.callback_query(lambda a: a.data == "Huyak_Cod", FSMCode.enter_full_name, DayFilter(is_day=True), flags=flags)
async def eter_full_name(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text="Укажите ФИО в формате: \"Фамилия Имя Очество\"")
    await state.set_state(FSMCode.enter_date)

@codeRouter.callback_query(lambda a: a.data == "Huyak_Cod", flags=flags)
async def day_except(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text="Денежный Код можно заказать только в Четверг")
    await state.clear()

@codeRouter.message(FSMCode.enter_date, flags=flags)
async def eter_date(message: Message, bot: Bot, state: FSMContext) -> None:
    await message.answer(
            text="Укажите дату рождения в формате 06.08.1987")
    await state.set_state(FSMCode.payment_code)

@codeRouter.message(DateFilter(is_date=True), FSMCode.payment_code, flags=flags)
async def order(message: Message, bot: Bot, state: FSMContext):
    await state.set_data({"date": message.text})
    await bot.send_invoice( 
                           chat_id=message.chat.id,
                           title="Денежный код",
                           description="Покупка услуги 'Денежный код'",
                           payload="Payment money code",
                           provider_token="381764678:TEST:61663",
                           currency="RUB",
                           prices=[
                               LabeledPrice(
                                   label="Денежный код",
                                   amount=39000,
                                   )])


@codeRouter.message(FSMCode.payment_code, flags=flags)
async def wrong_input(message: Message) -> None:
    if message.text == None:
        return
    await message.reply("Не правильный формат даты")

@codeRouter.pre_checkout_query()
async def pre_chechout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# @codeRouter.message(F.content_type.in_(ContentType.SUCCESSFUL_PAYMENT))
@codeRouter.message()
async def successful_payment(message: Message, bot: Bot, state: FSMContext) -> None:
    import pprint
    pprint.pprint(message.__doc__)
    data = await state.get_data()
    if message.text == None:
        return 
    result: str = await calculate_code(data['date'])
    await message.answer(result)

