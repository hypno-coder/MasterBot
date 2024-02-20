from database.connector import get_async_redis, users_db
from keyboards import get_mailing_button
from loader import bot, config


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
        self.__data = data
        self.message_settings = MessageBuilder.get_settings(self.__data)

    async def launch(self):
        self.redis = await get_async_redis()
        result = await self.__send_messages()
        await self.redis.close()
        return result

    async def __send_messages(self):
        users = await self.__get_users()
        new_users = users[:4]

        for user_id in new_users:
            sent_key = f"sent:{user_id}"
            already_sent = await self.redis.get(sent_key)
            if already_sent:
                continue
            try:
                await bot.send_message(user_id, **self.message_settings)
                await self.redis.set(sent_key, "true", self.DATA_EXPIRATION_TIME)
            except Exception as e:
                for admin_id in config.tg_bot.admin_ids:
                    await bot.send_message(
                        admin_id,
                        f"Ошибка при отправке сообщения пользователю {user_id}: {e} \n"
                        f"Отправленно {new_users.index(user_id)} сообщений",
                    )
                return "fail"

        return "complete"

    async def __get_users(self):
        users = await users_db.find({}).to_list(length=None)
        return [user["_id"] for user in users]
