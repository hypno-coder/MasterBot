import random
from enum import Enum
from asyncio import sleep
from aiogram.types.input_file import FSInputFile, BufferedInputFile

from loader import bot
from lexicon import CommonLexicon, PaidMenuButtons, CalendarLexicon, CodeLexicon, JantraLexicon
from keyboards.keyboards_generator import Keyboard 
from payment_services.user_data_type import UserDataType
from staticfiles import FilePath
from services import get_calendar_dates, calculate_code, Jantra

async def remove_message(chat_id: int, message_id: int, delay: int = 60) -> None:
    try:
        await sleep(delay)
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as ex:
        print(f'{CommonLexicon.remove_message_error} \n {ex}')

async def send_response(
        user_data: UserDataType,       
        min_delay: int = 1800, 
        max_delay: int = 4800,
        ) -> None:

    ITEMS_PER_ROW = 1
    chat_id = user_data['chat_id']
    fio = user_data['fio']
    birthday = user_data['birthday']

    reply_1 = await bot.send_message(
            chat_id,
            text=CommonLexicon.pay_success +' '+ CommonLexicon.message_delay + f'{round(min_delay/60)}-{round(max_delay/60)} минут', 
            reply_markup=Keyboard.create_inline(
                ITEMS_PER_ROW, backButton=PaidMenuButtons.BackToPaidMenu))
    delay = random.randint(min_delay, max_delay)
    await sleep(delay/2)
    try:
        await bot.delete_message(chat_id=reply_1.chat.id, message_id=reply_1.message_id)
    except Exception as ex:
        print(ex)
    reply_2 = await bot.send_message(
            chat_id,
            text=CommonLexicon.wait_result, 
            reply_markup=Keyboard.create_inline(
                ITEMS_PER_ROW, backButton=PaidMenuButtons.BackToPaidMenu))
    await sleep(delay/2)
    try:
        await bot.delete_message(chat_id=reply_2.chat.id, message_id=reply_2.message_id)
    except Exception as ex:
        print(ex)

    await bot.send_message(chat_id=chat_id, text='===========================')
    await bot.send_message(chat_id=chat_id, text=f'<i>{fio}</i>')

    match user_data['service_species']:
        case PaidMenuButtons.MoneyCalendar.name:
            calendar_doc = FSInputFile(FilePath.money_calendar_pdf.value)
            calendar_nubers: str = get_calendar_dates()
            calendar_result = ''.join(str(num) for num in calendar_nubers)
            await bot.send_message(chat_id=chat_id, text=f'<i>{PaidMenuButtons.MoneyCalendar.value}</i>')
            await bot.send_document(chat_id, calendar_doc, caption=CalendarLexicon.document)
            await bot.send_message(chat_id, f'<b>{CalendarLexicon.for_you}</b> {calendar_result}')

        case PaidMenuButtons.MoneyCode.name:
            code_doc = FSInputFile(FilePath.money_code_pdf.value)
            code_video = FSInputFile(FilePath.money_code_video.value)
            code_result: str = await calculate_code(birthday) 
            await bot.send_message(chat_id=chat_id, text=f'<i>{PaidMenuButtons.MoneyCode.value}</i>')
            await bot.send_document(chat_id, code_doc, caption=CodeLexicon.document)
            await bot.send_message(chat_id, f'<b>{CodeLexicon.for_you}</b> {code_result}')
            await bot.send_video(chat_id, code_video)

        case PaidMenuButtons.Jantra.name:
            image, number = Jantra.create(birthday)
            input_image = BufferedInputFile(image, 'jantra.png')
            await bot.send_message(chat_id=chat_id, text=f'<i>{PaidMenuButtons.Jantra.value}</i>')
            await bot.send_photo(chat_id, input_image)
            await bot.send_message(chat_id, f'<b>{JantraLexicon.lucky_number+str(number)}</b>')

        case _:
            pass

    await bot.send_message(chat_id=chat_id, text='===========================')
    await bot.send_message(
            chat_id, 
            text=CommonLexicon.back_menu, 
            reply_markup=Keyboard.create_inline(
                ITEMS_PER_ROW, backButton=PaidMenuButtons.BackToPaidMenu)) 

async def send_message_with_delay(
        chat_id: int, 
        name: str,
        back_button_callback: Enum | None = None,
        min_delay: int = 1800, 
        max_delay: int = 4800,
        greeting: str | None = None,
        text: str | None = None,
        image: BufferedInputFile | None = None,
        video: FSInputFile | None = None,
        document:  FSInputFile | None = None,
        document_caption: str = ''
        ) -> None:

    def get_keyboard():
        ITEMS_PER_ROW = 1
        if back_button_callback != None:
            return Keyboard.create_inline(ITEMS_PER_ROW, backButton=back_button_callback) 
        return None

    reply = await bot.send_message(
            chat_id,
            text=CommonLexicon.pay_success +' '+ CommonLexicon.message_delay + f'{round(min_delay/60)}-{round(max_delay/60)} минут', 
            reply_markup=get_keyboard())

    delay = random.randint(min_delay, max_delay)
    await sleep(delay)
    try:
        await bot.delete_message(chat_id=reply.chat.id, message_id=reply.message_id)
    except Exception as ex:
        print(ex)
    await bot.send_message(chat_id=chat_id, text='===========================')
    await bot.send_message(chat_id=chat_id, text=f'<b>{name}</b>')

    if greeting != None:
        await bot.send_message(chat_id=chat_id, text=f'<i>{greeting}</i>')
    if image != None:
        await bot.send_photo(chat_id, image)
    if text != None:
        await bot.send_message(chat_id, text)
    if document != None:
        await bot.send_document(chat_id, document, caption=document_caption)
    if video != None:
        await bot.send_video(chat_id, video)

    await bot.send_message(chat_id=chat_id, text='===========================')

    await bot.send_message(chat_id, text=CommonLexicon.back_menu, reply_markup=get_keyboard()) 
