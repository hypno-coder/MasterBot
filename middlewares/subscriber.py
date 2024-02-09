from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from keyboards import subscribe_keyboard 
from lexicon import MiddlewareLexicon 
from loader import bot, config



class SubscriberMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:        
        if not isinstance(event, (Message, CallbackQuery)):
            return
        if event.from_user == None:
            return
        user = await bot.get_chat_member(
                chat_id=config.tg_bot.subscribe_channel,
                user_id=event.from_user.id)
        if user.status != MiddlewareLexicon.status:
            return await handler(event, data)

        await event.answer(
                text=MiddlewareLexicon.alert, 
                reply_markup=subscribe_keyboard)
