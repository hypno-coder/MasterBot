import random
from asyncio import sleep
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.input_file import FSInputFile, BufferedInputFile

from loader import bot
from lexicon import BotText
from keyboards.keyboards_generator import create_inline_kb

async def remove_message(chat_id: int, message_id: int, delay: int = 60) -> None:
    try:
        await sleep(delay)
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as ex:
        print(f'{BotText.remove_message_error} \n {ex}')

async def send_message_with_delay(
        chat_id: int, 
        name: str,
        back_button_callback: str | None = None,
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
            return create_inline_kb(ITEMS_PER_ROW, back_button_callback) 
        return None

    reply = await bot.send_message(
            chat_id,
            text=BotText.pay_success +' '+ BotText.message_delay + f'{round(min_delay/60)}-{round(max_delay/60)} минут', 
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

    await bot.send_message(chat_id, text=BotText.back_menu, reply_markup=get_keyboard()) 
