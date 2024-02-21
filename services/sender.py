from asyncio import create_task

from aiogram.exceptions import TelegramBadRequest

from database.connector import get_async_redis, users_db
from keyboards import get_mailing_button
from loader import bot, config
from utils import remove_message


class MessageBuilder:
    def __init__(self, data):
        self.bot = bot
        self.mailing_name = data["mailing_name"]
        self.mailing_message = data["mailing_message"]
        self.button = {"name": data["button_name"], "link": data["button_link"]}

    @classmethod
    def get_settings(cls, data):
        return cls(data).__setup_settings()

    def __setup_settings(self):
        return {
            "text": (
                f"<code>{self.mailing_message}</code>"
                if self.mailing_name == "0"
                else f"<b>{self.mailing_name}</b>\n<code>{self.mailing_message}</code>"
            ),
            "reply_markup": (
                None
                if self.button["name"] == None
                else get_mailing_button(self.button["name"], self.button["link"])
            ),
        }


class Mailing:
    DATA_EXPIRATION_TIME = 21600
    admin_list = config.tg_bot.admin_ids

    def __init__(self, data):
        self.bot = bot
        self.message_settings = MessageBuilder.get_settings(data)
        self.__photo_id = data["photo_id"]
        self.__delay = int(data["delay"]) * 60

    async def launch(self):
        self.redis = await get_async_redis()
        result = await self.__send_messages()
        await self.redis.close()
        return result

    async def __send_messages(self):
        users = await self.__get_users()
        for user_id in users:
            sent_key = f"sent:{user_id}"
            already_sent = await self.redis.get(sent_key)
            if already_sent:
                continue
            try:
                if self.__photo_id != "0":
                    resp_photo = await bot.send_photo(user_id, self.__photo_id)
                    create_task(
                        remove_message(
                            chat_id=resp_photo.chat.id,
                            message_id=resp_photo.message_id,
                            delay=self.__delay,
                        )
                    )
                resp_message = await bot.send_message(user_id, **self.message_settings)
                create_task(
                    remove_message(
                        chat_id=resp_message.chat.id,
                        message_id=resp_message.message_id,
                        delay=self.__delay,
                    )
                )
                await self.redis.set(sent_key, "true", self.DATA_EXPIRATION_TIME)
            except TelegramBadRequest as e:
                if "chat not found" in str(e):
                    for admin_id in config.tg_bot.admin_ids:
                        await bot.send_message(
                            admin_id,
                            f"Ошибка при отправке сообщения пользователю {user_id}: {e} \n"
                            f"Отправленно {users.index(user_id)} сообщений",
                        )
                        continue
                else:
                    return e
            except Exception as e:
                return e
        return "complete"

    async def __get_users(self):
        users = await users_db.find({}).to_list(length=None)
        return [user["_id"] for user in users]
