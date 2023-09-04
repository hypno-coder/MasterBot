from typing import cast
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from keyboards import calendar_action_menu_keyboard
from loader import payment
from aiogram.filters import Text 
from staticfiles import FilePath
from keyboards import BotCBData
from lexicon import BotText 
from config_data import SpamConfig
from states import FSMCalendar
from services import get_calendar_dates 
from utils import send_message_with_delay

calendarHandlerRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.calendar_menu.name}


@calendarHandlerRouter.callback_query(
        lambda a: a.data == BotCBData.MoneyCalendarBtn2.value, flags=flags)
@calendarHandlerRouter.callback_query(lambda a: a.data == BotCBData.MoneyCalendarBtn4.value, flags=flags)
async def enter_full_name(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=BotText.enter_fio)
    await state.set_state(FSMCalendar.enter_date)


@calendarHandlerRouter.message(~Text(contains=['/']), FSMCalendar.enter_date, flags=flags)
async def enter_date(message: Message, state: FSMContext) -> None:
    if message.text == None or message.from_user == None:
        return

    fio: str = message.text 
    await state.set_data({'fio': fio})

    await message.answer(text=BotText.enter_date)
    await state.set_state(FSMCalendar.check_data)


@calendarHandlerRouter.message(~Text(contains=['/']), FSMCalendar.check_data, flags=flags)
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
    await message.answer(
            text=BotText.selected_action, 
            reply_markup=calendar_action_menu_keyboard)

    

@calendarHandlerRouter.callback_query(
        lambda a: a.data == BotCBData.MoneyCalendarBtn3.value,
        flags=flags)
async def order(callback: CallbackQuery, bot: Bot, state: FSMContext):
    callback.answer()
    message = callback.message
    if message == None: 
        return

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
        ~Text(contains=['/']),
        F.content_type.in_(ContentType.SUCCESSFUL_PAYMENT), FSMCalendar.successful_payment, flags=flags)
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
            back_button_callback=BotCBData.BackToPaidMenu.name,
            greeting=fio,
            document=document, 
            document_caption=BotText.money_calendar_document,
            text=f'<b>{BotText.money_calendar_for_you}</b> {result}')
