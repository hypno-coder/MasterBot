from typing import cast
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from keyboards import calendar_action_menu_keyboard
from loader import payment
from staticfiles import FilePath
from lexicon import CalendarMenuButtons, CalendarActionMenuButtons, CommonLexicon, CalendarLexicon, PaidMenuButtons 
from config_data import SpamConfig
from states import FSMCalendar
from filters import DateFilter, AgeFilter
from services import get_calendar_dates 
from utils import send_message_with_delay


calendarHandlerRouter: Router = Router()
flags: dict[str, str] = {'throttling_key': SpamConfig.calendar_menu.name}


@calendarHandlerRouter.callback_query(F.data.in_([
   CalendarMenuButtons.CalculateMoneyCalendar.name,
    CalendarActionMenuButtons.CalendarEditData.name]), flags=flags)
async def enter_full_name(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=CommonLexicon.enter_fio)
    await state.set_state(FSMCalendar.enter_date)


@calendarHandlerRouter.message(~F.text.startswith('/'), FSMCalendar.enter_date, flags=flags)
async def enter_date(message: Message, state: FSMContext) -> None:
    if message.text == None or message.from_user == None:
        return

    fio: str = message.text 
    await state.set_data({'fio': fio})

    await message.answer(text=CommonLexicon.enter_date)
    await state.set_state(FSMCalendar.check_data)


@calendarHandlerRouter.message(
        ~F.text.startswith('/'), 
        FSMCalendar.check_data, 
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
    await message.answer(
            text=CommonLexicon.selected_action, 
            reply_markup=calendar_action_menu_keyboard)


@calendarHandlerRouter.message(
        ~F.text.startswith('/'), 
        FSMCalendar.check_data, 
        DateFilter(is_date=True), 
        flags=flags)
async def wrong_age(message: Message) -> None:
    if message.text == None:
        return

    await message.reply(CommonLexicon.legal_age)


@calendarHandlerRouter.message(~F.text.startswith('/'), FSMCalendar.check_data, flags=flags)
async def wrong_input(message: Message) -> None:
    if message.text == None:
        return

    await message.reply(CommonLexicon.invalid_format_date)


@calendarHandlerRouter.callback_query(
        F.data == CalendarActionMenuButtons.CalendarConfirmData.name, 
        flags=flags)
async def order(callback: CallbackQuery, bot: Bot, state: FSMContext):
    callback.answer()
    message = callback.message
    if message == None: 
        return

    await bot.send_invoice( 
                           chat_id=message.chat.id,
                           title=CalendarLexicon.label,
                           description=CalendarLexicon.description,
                           payload=CalendarLexicon.payload,
                           provider_token=payment.yoomoney.token,
                           currency=payment.currency,
                           prices=[
                               LabeledPrice(
                                   label=CalendarLexicon.label,
                                   amount=int(str(payment.price.money_calendar) + '00'),
                                   )])
                               
    await state.set_state(FSMCalendar.checkout_query)


@calendarHandlerRouter.pre_checkout_query(FSMCalendar.checkout_query, flags=flags)
async def pre_chechout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await state.set_state(FSMCalendar.successful_payment)


@calendarHandlerRouter.message(
        ~F.text.startswith('/'),
        F.content_type.in_(ContentType.SUCCESSFUL_PAYMENT), 
        FSMCalendar.successful_payment, 
        flags=flags)
async def successful_payment(message: Message, state: FSMContext) -> None:
    if message.from_user == None: 
        return

    chat_id: int = message.chat.id
    numbers: str = get_calendar_dates()
    result = ''.join(str(num) for num in numbers)
    data: dict = await state.get_data() 
    fio: str = data['fio'] 
    document = FSInputFile(FilePath.money_calendar_pdf.value)

    await send_message_with_delay(
            chat_id, 
            name=CalendarLexicon.label,
            back_button_callback=PaidMenuButtons.BackToPaidMenu,
            greeting=fio,
            document=document, 
            document_caption=CalendarLexicon.document,
            text=f'<b>{CalendarLexicon.for_you}</b> {result}')
