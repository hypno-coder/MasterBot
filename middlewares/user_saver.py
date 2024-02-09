from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from database import User 
from lexicon import MiddlewareLexicon 
from loader import bot, config

class UserSaverMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return
        
        if event.from_user == None or event.text != '/start':
            return await handler(event, data)

        self.user = User(event.from_user)
        self.username = event.from_user.username
        try:
            result, is_user = await self.user.get_or_create()
            data['status'] = result['status']
            
            if is_user == 'create':
                await self.send_message()
            if is_user == 'get': 
                await self.user.date_update() 
        except Exception as ex:
            print(ex) 
        finally:
            return await handler(event, data)


    async def send_message(self):
        count = await self.user.total_count()
        for admin_id in config.tg_bot.admin_ids:
            await bot.send_message(
                    chat_id=admin_id, 
                    text=f"""{MiddlewareLexicon.new_user} - {self.username} \n
                    {MiddlewareLexicon.total_users}{count}""")
