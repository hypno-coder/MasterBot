import asyncio
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, F
from aiogram.types import CallbackQuery, Message, TelegramObject

from lexicon import MiddlewareLexicon
from loader import bot, config
from services import BotAccessController
from utils import remove_message


class BotLockCheckerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, (Message, CallbackQuery)):
            return
        if event.from_user == None:
            return
        if event.from_user.id in config.tg_bot.admin_ids:
            return await handler(event, data)

        chat_id: int = 0
        if isinstance(event, Message):
            chat_id: int = event.chat.id
        if isinstance(event, CallbackQuery):
            if event.message == None:
                return
            chat_id: int = event.message.chat.id

        controller = BotAccessController()
        result = await controller.is_locked()
        if result:
            reply = await bot.send_message(
                chat_id=chat_id, text=MiddlewareLexicon.technical_works
            )
            asyncio.create_task(
                remove_message(chat_id=chat_id, message_id=reply.message_id, delay=20)
            )
            return
        return await handler(event, data)
