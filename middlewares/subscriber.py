from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from aiogram.types.input_file import FSInputFile

from database.connector import get_async_redis
from keyboards import subscribe_keyboard
from lexicon import MiddlewareLexicon
from loader import bot, config
from staticfiles import FilePath


class SubscriberMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, (Message, CallbackQuery)):
            return await handler(event, data)

        if not event.from_user:
            return await handler(event, data)

        user = await bot.get_chat_member(
            chat_id=config.tg_bot.subscribe_channel, user_id=event.from_user.id
        )

        if user.status != MiddlewareLexicon.status:
            return await handler(event, data)

        if isinstance(event, Message):
            await self.__greeting_sender(event)
        await event.answer(
            text=MiddlewareLexicon.alert, reply_markup=subscribe_keyboard
        )

    async def __greeting_sender(self, event: Message):
        assert event.chat.id
        chat_id = event.chat.id
        try:
            self.redis = await get_async_redis()
            await self.__send_video_by_id(chat_id)
        except Exception:
            await self.__send_video_from_file(chat_id)

    async def __send_video_from_file(self, chat_id):
        greeting_video = FSInputFile(FilePath.greeting.value)
        result = await bot.send_video_note(chat_id, greeting_video)
        if result.video_note is not None:
            await self.redis.set("greeting_id", result.video_note.file_id)

    async def __send_video_by_id(self, chat_id):
        greeting_id = await self.redis.get("greeting_id")
        assert greeting_id
        await bot.send_video_note(chat_id, greeting_id.decode())
