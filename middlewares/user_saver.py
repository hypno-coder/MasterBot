from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from database import add_user, get_user, update_date_user, get_total_users_count
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

        user = await get_user(event.from_user.id)

        if user == None:
            result = await add_user(event.from_user) 
            count = await get_total_users_count()
            if result:
                for admin_id in config.tg_bot.admin_ids:
                    await bot.send_message(
                            chat_id=admin_id, 
                            text=f"{BotText.user_saver['text1']} - {event.from_user.username} \n{BotText.user_saver['text2']} {count}")

            return await handler(event, data)

        else: 
            await update_date_user(event.from_user.id, user['last_visit_date'])
            return await handler(event, data)

        

