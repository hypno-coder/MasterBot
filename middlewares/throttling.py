from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message, CallbackQuery, TelegramObject

from loader import bot 
from config_data import genTrotCash
from lexicon import MiddlewareLexicon 
from utils import remove_message


class ThrottlingMiddleware(BaseMiddleware):
    # TODO: genThrotCash
    caches = genTrotCash()
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, (Message, CallbackQuery)):
            return

        chat_id: int = 0
        if isinstance(event, Message):
            chat_id: int = event.chat.id
        if isinstance(event, CallbackQuery):
            if event.message == None: return
            chat_id: int = event.message.chat.id


        throttling_key = get_flag(data, "throttling_key")
        if throttling_key is not None and throttling_key in self.caches:
            if chat_id in self.caches[throttling_key]:
                reply = await bot.send_message(chat_id=chat_id, text=MiddlewareLexicon.stop_spam) 
                await remove_message(chat_id=chat_id, message_id=reply.message_id, delay=10)
                return
            else:
                self.caches[throttling_key][chat_id] = None

        return await handler(event, data)
