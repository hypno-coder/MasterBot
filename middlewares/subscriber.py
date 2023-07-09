from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from keyboards import sub_inline_keyboard, sub_common_keyboard 
from database import add_user
from lexicon import BotText 
from loader import bot, config
from pprint import pprint

EventType = Message | CallbackQuery 


class Subscriber(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[EventType, Dict[str, Any]], Awaitable[Any]],
        event: EventType,
        data: Dict[str, Any]
    ) -> Any:
        
        if event.from_user == None:
            return
        await add_user(event.from_user) 
        user = await bot.get_chat_member(
                chat_id=config.tg_bot.subscribe_channel,
                user_id=event.from_user.id)

        pprint(event.from_user)
        if user.status != "left":
            result = await handler(event, data)
            return result

        await event.answer(
                text= BotText.subscriber['inline_text'],
                reply_markup=sub_inline_keyboard)
        await bot.send_message(
                chat_id=event.from_user.id, 
                text=BotText.subscriber['common_text'], 
                reply_markup=sub_common_keyboard)

