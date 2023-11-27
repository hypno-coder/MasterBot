from aiogram import Bot

from database import User
from database.connector import redis_db
from keyboards import get_mailing_button
from errors import send_error_message
from loader import config

class Sender: 
    __error_count = 0
    __mailing_count = 0

    def __init__(self, bot: Bot, data):
        self.bot = bot
        self.mailing_data = data

    async def start(self):
        users = await User.get_all()
        loop_count = 0
        try:
            for user in users[self.__mailing_count:4]:
                await self.__mailing(user)
                loop_count += 1
                redis_db.setex('mailing_count', 86400, loop_count)
        except:
            self.__error_count += 1
            if self.__error_count == 5:
                await send_error_message(f'Ошибка рассылки! Разослали {self.__mailing_count} / {len(users)+1}')
                return

            count_bytes = redis_db.get('mailing_count')
            count = int(count_bytes.decode('utf-8')) if count_bytes else 0

            if count is not None:
                # +2 потому что список с 0 начинается и рассылку нужно начать со следующего пользователя
                self.__mailing_count = int(count) + 2

            await self.start()

        else:
            count_bytes = redis_db.get('mailing_count')
            count = int(count_bytes.decode('utf-8')) if count_bytes else 0
            for admin_id in config.tg_bot.admin_ids:
                await self.bot.send_message(
                    chat_id=admin_id, 
                    text=f'Рассылка завершена! Разослали {count} / {len(users)+1}')


    async def __mailing(self, user):
        await self.bot.send_message(chat_id=user['_id'], text=f'Приветствую {user["username"]}!')
        if self.mailing_data['photo_id'] != '0':
            await self.bot.send_photo(user['_id'], self.mailing_data['photo_id'])
        await self.bot.send_message(chat_id=user['_id'], text=self.mailing_data["mailing_message"])
        if self.mailing_data['button_name'] is not None:
            await self.bot.send_message(
                    chat_id=user['_id'], 
                    text=self.mailing_data["mailing_message"],
                    reply_markup=get_mailing_button(
                        self.mailing_data['button_name'], 
                        self.mailing_data['button_link']))


    def __save_mailing_state(self):
        pass



    

       
