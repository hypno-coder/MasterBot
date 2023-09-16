from typing import cast
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from keyboards import code_action_menu_keyboard
from loader import payment
from staticfiles import FilePath
from lexicon import CommonLexicon, CodeLexicon, CodeMenuButtons, CodeActionMenuButtons, PaidMenuButtons 
from filters import DayFilter
from config_data import SpamConfig
from states import FSMCode
from filters import DateFilter, AgeFilter
from services import calculate_code
from utils import send_message_with_delay

codeHandlerRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.code_menu.name}


@codeHandlerRouter.callback_query(
        DayFilter(is_day=True), 
        F.data.in_([CodeMenuButtons.CalculateMoneyCode.name, CodeActionMenuButtons.CodeEditData.name]), 
        flags=flags)
async def enter_full_name(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=CommonLexicon.enter_fio) 
    await state.set_state(FSMCode.enter_date)


@codeHandlerRouter.callback_query(F.data.in_([
    CodeMenuButtons.CalculateMoneyCode.name, CodeActionMenuButtons.CodeEditData.name]), flags=flags)
async def day_except(callback: CallbackQuery, state: FSMContext) -> None:
    callback.answer()
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=CodeLexicon.only_thursday)
    await state.clear()


@codeHandlerRouter.message(~F.text.startswith('/'), FSMCode.enter_date, flags=flags)
async def enter_date(message: Message, state: FSMContext) -> None:
    if message.text == None or message.from_user == None:
        return

    fio: str = message.text 
    await state.set_data({'fio': fio})

    await message.answer(text=CommonLexicon.enter_date)
    await state.set_state(FSMCode.check_data)


@codeHandlerRouter.message(
        ~F.text.startswith('/'),
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

    await message.answer(text=CommonLexicon.check_data)
    await message.answer(text=f'{CommonLexicon.fio}{fio}')
    await message.answer(text=f'{CommonLexicon.birthday}{birthday}')
    await message.answer(text=CommonLexicon.selected_action, reply_markup=code_action_menu_keyboard)


@codeHandlerRouter.message(~F.text.startswith('/'), FSMCode.check_data, DateFilter(is_date=True), flags=flags)
async def wrong_age(message: Message) -> None:
    if message.text == None:
        return

    await message.reply(CommonLexicon.legal_age)


@codeHandlerRouter.message(~F.text.startswith('/'), FSMCode.check_data, flags=flags)
async def wrong_input(message: Message) -> None:
    if message.text == None:
        return
    await message.reply(CommonLexicon.invalid_format_date)


@codeHandlerRouter.callback_query(F.data == CodeActionMenuButtons.CodeConfirmData.name, flags=flags)
async def order(callback: CallbackQuery, bot: Bot, state: FSMContext):
    callback.answer()
    message = callback.message
    if message == None: 
        return

    await bot.send_invoice( 
                           chat_id=message.chat.id,
                           title=CodeLexicon.label,
                           description=CodeLexicon.payment_description,
                           payload=CodeLexicon.payload,
                           provider_token=payment.yoomoney.token,
                           currency=payment.currency,
                           prices=[
                               LabeledPrice(
                                   label=CodeLexicon.label,
                                   amount=int(str(payment.price.money_code) + '00'),
                                   )])
                               
    await state.set_state(FSMCode.checkout_query)


@codeHandlerRouter.pre_checkout_query(FSMCode.checkout_query, flags=flags)
async def pre_chechout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await state.set_state(FSMCode.successful_payment)


@codeHandlerRouter.message(
        ~F.text.startswith('/'),
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
            name=CodeLexicon.label,
            back_button_callback=PaidMenuButtons.BackToPaidMenu,
            text=f'<b>{CodeLexicon.for_you+result}</b>',
            greeting=fio,
            video=video, 
            document=document, 
            document_caption=CodeLexicon.document)
