import logging
import json
import uvicorn

from aiogram import types

from loader import config, bot, dp, app
from handlers import mainRouter
from middlewares import SubscriberMiddleware, UserSaverMiddleware, ThrottlingMiddleware 
from database.connector import redis_db
from commands import set_command_menu
from utils import send_response


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)


WEBHOOK_PATH = f'/bot/{config.tg_bot.token}'
WEBHOOK_URL = f'{config.tg_bot.base_url}{WEBHOOK_PATH}'


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info != WEBHOOK_URL:
        try:
            await bot.set_webhook(url=WEBHOOK_URL)
            await set_command_menu(bot)
        except Exception as ex:
            print(f'Отвалил сервер телеги - \n{ex}')
    logger.info("Bot started")


dp.message.middleware(SubscriberMiddleware())
dp.callback_query.middleware(SubscriberMiddleware())
dp.message.middleware(UserSaverMiddleware())
dp.message.middleware(ThrottlingMiddleware())


try:
    dp.include_router(mainRouter)
except Exception as ex:
    print(f'ОШИБКА БОТА - \n{ex}')


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


@app.get(WEBHOOK_PATH+'/payment')
async def bot_webhook_payment(
        out_summ,
        OutSum,
        inv_id,
        InvId,
        crc,
        SignatureValue,
        PaymentMethod,
        IncSum,
        IncCurrLabel,
        EMail,
        Fee,
        ):
    user_data = redis_db.get(str(InvId))
    if user_data:
        await send_response(json.loads(user_data))
        return f'OK{InvId}'
    return 'bad sign'

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
    logger.info("Bot stopped")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
