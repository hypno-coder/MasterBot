import asyncio
from aiogram import Bot

from database import User
from database.connector import redis_db
from keyboards import get_mailing_button
from errors import send_error_message
from loader import config

class Sender: 
    __error_count = 0
    __loop_count = 0
    __mailing_count = 0
    __number_of_attempts = 0

    def __init__(self, bot: Bot, data):
        self.bot = bot
        self.mailing_data = data

    async def start(self):
        users = await User.get_all()
        try:
            await self.__mailing_loop(users)
        except Exception:
            print(f'Ошибка рассылки (попытка {self.__error_count})')
            await self.__error_action(users)
        else:
            await self.__mailing_complete_action(users)
            

    async def __mailing_complete_action(self, users):
        count = self.__get_mailing_count()
        for admin_id in config.tg_bot.admin_ids:
            await self.bot.send_message(
                chat_id=admin_id, 
                text=f'Рассылка завершена! Разослали {count} / {len(users)+1}')


    async def __error_action(self, users):
        DELAY_BEFORE_REPEATING = 3
        self.__error_count += 1
        count = self.__get_mailing_count()
        if count is not None:
            self.__mailing_count = int(count)
        
        if self.__error_count < self.__number_of_attempts:
            await asyncio.sleep(DELAY_BEFORE_REPEATING)
            return await self.start()
        else:
            await send_error_message(f'Ошибка рассылки! Разослали {self.__mailing_count} / {len(users)+1}')


    async def __mailing_loop(self, users):
        for user in users[self.__mailing_count:]:
            self.__loop_count += 1
            await self.__mailing(user)
            redis_db.setex('mailing_count', 86400, self.__loop_count)


    async def __mailing(self, user):
        await self.bot.send_message(chat_id=user['_id'], text=f'Приветствую {user["username"]}!')
        if self.mailing_data['photo_id'] != '0':
            await self.bot.send_photo(user['_id'], self.mailing_data['photo_id'])
        if self.mailing_data['button_name'] is None:
            await self.bot.send_message(chat_id=user['_id'], text=self.mailing_data['mailing_message'])
        if self.mailing_data['button_name'] is not None:
            await self.bot.send_message(
                    chat_id=user['_id'], 
                    text=self.mailing_data['mailing_message'],
                    reply_markup=get_mailing_button(
                        self.mailing_data['button_name'], 
                        self.mailing_data['button_link']))


    def __get_mailing_count(self):
        count_bytes = redis_db.get('mailing_count')
        return int(count_bytes.decode('utf-8')) if count_bytes else 0
