import asyncio
import json
import logging
import hmac

import uvicorn
from aiogram import types
from http import HTTPStatus
from fastapi import Request 

from commands import set_command_menu
from database.connector import redis_db
from handlers import mainRouter
from loader import app, bot, dp
from payment_services import ProdamusClient
from middlewares import (BotLockCheckerMiddleware, SubscriberMiddleware,
                         ThrottlingMiddleware, UserSaverMiddleware)
from services import ResponseController
from url_const import WEBHOOK_PATH, WEBHOOK_URL

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
)


@app.on_event("startup")
async def on_startup():
    print(WEBHOOK_URL)
    webhook_info = await bot.get_webhook_info()
    if webhook_info != WEBHOOK_URL:
        try:
            await bot.set_webhook(url=WEBHOOK_URL)
            await set_command_menu(bot)
        except Exception as ex:
            print(f"Отвалил сервер телеги - \n{ex}")
    logger.info("Bot started")


dp.message.middleware(SubscriberMiddleware())
dp.callback_query.middleware(SubscriberMiddleware())
dp.message.middleware(UserSaverMiddleware())
dp.message.middleware(BotLockCheckerMiddleware())
dp.callback_query.middleware(BotLockCheckerMiddleware())
dp.message.middleware(ThrottlingMiddleware())


try:
    dp.include_router(mainRouter)
except Exception as ex:
    print(f"ОШИБКА БОТА - \n{ex}")


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


@app.get(WEBHOOK_PATH + "/payment")
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
    if user_data is None:
        return "bad sign"

    response = ResponseController(user_data=json.loads(user_data))
    asyncio.create_task(response.launch())
    return f"OK{InvId}"


@app.post("/prodamus")
async def prodamus_webhook(request: Request):
    sign_header = request.headers.get("Sign")
    if not sign_header:
        return HTTPStatus.BAD_REQUEST

    try:
        data = await request.json()
    except Exception:
        return HTTPStatus.BAD_REQUEST

    prodamus = ProdamusClient("webhook")
    expected = prodamus.make_signature(data) 

    if not hmac.compare_digest(expected, sign_header):
        return HTTPStatus.FORBIDDEN

    user_data = redis_db.get(data["_param_id"])
    if user_data is None:
        return HTTPStatus.FORBIDDEN

    response = ResponseController(user_data=json.loads(user_data))
    asyncio.create_task(response.launch())
    return HTTPStatus.OK


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
    logger.info("Bot stopped")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
