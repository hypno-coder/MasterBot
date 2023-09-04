from typing import cast
from aiogram import Router, Bot, F
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from keyboards import code_action_menu_keyboard
from loader import payment
from staticfiles import FilePath
from keyboards import BotCBData
from lexicon import BotText 
from config_data import SpamConfig
from states import FSMCode
from filters import DateFilter, AgeFilter
from services import calculate_code
from utils import send_message_with_delay

codeHandlerRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.code_menu.name}


@codeHandlerRouter.callback_query(
        lambda a: a.data == BotCBData.MoneyCodeBtn2.value, flags=flags)
@codeHandlerRouter.callback_query(lambda a: a.data == BotCBData.MoneyCodeBtn4.value, flags=flags)
async def enter_full_name(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=BotText.enter_fio) 
    await state.set_state(FSMCode.enter_date)


@codeHandlerRouter.message(~Text(contains=['/']), FSMCode.enter_date, flags=flags)
async def enter_date(message: Message, state: FSMContext) -> None:
    if message.text == None or message.from_user == None:
        return

    fio: str = message.text 
    await state.set_data({'fio': fio})

    await message.answer(text=BotText.enter_date)
    await state.set_state(FSMCode.check_data)


@codeHandlerRouter.message(
        ~Text(contains=['/']),
        FSMCode.check_data,
        DateFilter(is_date=True), 
        AgeFilter(is_age=True), 
        flags=flags)
async def check_data(message: Message, state: FSMContext) -> None:
    if message.text == None or message.from_user == None:
        return

    data = await state.get_data() 
    fio: str = data['fio']
    birthday: str = message.text 
    data.update({'birthday': birthday})
    await state.update_data(data)

    await message.answer(text=BotText.check_data)
    await message.answer(text=f'{BotText.fio}{fio}')
    await message.answer(text=f'{BotText.birthday}{birthday}')
    await message.answer(text=BotText.selected_action, reply_markup=code_action_menu_keyboard)


@codeHandlerRouter.message(~Text(contains=['/']), FSMCode.check_data, DateFilter(is_date=True), flags=flags)
async def wrong_age(message: Message) -> None:
    if message.text == None:
        return

    await message.reply(BotText.legal_age)


@codeHandlerRouter.message(~Text(contains=['/']), FSMCode.check_data, flags=flags)
async def wrong_input(message: Message) -> None:
    if message.text == None:
        return
    await message.reply(BotText.invalid_format_date)


@codeHandlerRouter.callback_query(
        lambda a: a.data == BotCBData.MoneyCodeBtn3.value, 
        flags=flags)
async def order(callback: CallbackQuery, bot: Bot, state: FSMContext):
    callback.answer()
    message = callback.message
    if message == None: 
        return

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


@codeHandlerRouter.pre_checkout_query(FSMCode.checkout_query, flags=flags)
async def pre_chechout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await state.set_state(FSMCode.successful_payment)


@codeHandlerRouter.message(
        ~Text(contains=['/']),
        F.content_type.in_(ContentType.SUCCESSFUL_PAYMENT), FSMCode.successful_payment, flags=flags)
async def successful_payment(message: Message, state: FSMContext) -> None:
    if message.from_user == None: 
        return

    chat_id: int = message.chat.id
    data: dict = await state.get_data() 
    fio: str = data['fio'] 
    birthday: str = data['birthday'] 
    result: str = await calculate_code(birthday) 
    document = FSInputFile(FilePath.money_code_pdf.value)
    video = FSInputFile(FilePath.money_code_video.value)

    await send_message_with_delay(
            chat_id, 
            name=BotText.money_code_title,
            back_button_callback=BotCBData.BackToPaidMenu.name,
            text=f'<b>{BotText.money_code_for_you+result}</b>',
            greeting=fio,
            video=video, 
            document=document, 
            document_caption=BotText.money_code_document)
