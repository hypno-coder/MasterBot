from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from database import User 
from lexicon import BotText
from loader import bot, config

EventType = Message | CallbackQuery 


class UserSaver(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[EventType, Dict[str, Any]], Awaitable[Any]],
        event: EventType,
        data: Dict[str, Any]
    ) -> Any:

        if event.from_user == None:
            return

        user = User(event.from_user)
        request_status = await user.get()

        if request_status == None:
            result = await user.add() 
            count = await user.total_count()
            if result:
                for admin_id in config.tg_bot.admin_ids:
                    await bot.send_message(
                            chat_id=admin_id, 
                            text=f"{BotText.user_saver['text1']} - {event.from_user.username} \n{BotText.user_saver['text2']} {count}")

            return await handler(event, data)

        else: 
            await user.date_update() 
            return await handler(event, data)

        

