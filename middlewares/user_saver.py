from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from database import User 
from lexicon import BotText
from loader import bot, config

class UserSaverMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
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
                    text=f"""{BotText.user_saver['text1']} - {self.username} \n
                    {BotText.user_saver['text2']} {count}""")





        

