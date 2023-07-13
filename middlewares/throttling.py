from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message

from loader import bot 
from config_data import genTrotCash


class ThrottlingMiddleware(BaseMiddleware):
    caches = genTrotCash()
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:

        throttling_key = get_flag(data, "throttling_key")
        if throttling_key is not None and throttling_key in self.caches:
            if event.chat.id in self.caches[throttling_key]:
                await bot.send_message(chat_id=event.chat.id,text='нельзя часто  спамить =)') 
                return
            else:
                self.caches[throttling_key][event.chat.id] = None
        return await handler(event, data)
