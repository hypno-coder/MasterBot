from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from keyboards import subscriber_keyboard
from loader import bot, config

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
        user = await bot.get_chat_member(
                chat_id=config.tg_bot.subscribe_channel,
                user_id=event.from_user.id)
        if user.status != "left":
            result = await handler(event, data)
            return result
        await event.answer(
                text='Для начала работы с ботом, нужно быть подписанным на канал: Мастерская Желаний', 
                reply_markup=subscriber_keyboard)

