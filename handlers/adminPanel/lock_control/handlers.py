import asyncio

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery

from config_data import SpamConfig
from lexicon import LockControlMenuButtons
from loader import config
from services import BotAccessController
from utils import remove_message

lockСontrolHandlerRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.lock_control_menu.name}


@lockСontrolHandlerRouter.callback_query(
    F.data == LockControlMenuButtons.BotBlocking.name,
    F.from_user.id.in_(config.tg_bot.admin_ids),
)
async def block_bot(callback: CallbackQuery, bot: Bot) -> None:
    callback.answer()
    if callback.message == None:
        return

    controller = BotAccessController()
    result = await controller.lock()
    text: str = ""
    if not result:
        text = "Блокировка бота не удалась"
    text = "Бот Заблокирован"
    data = await bot.send_message(chat_id=callback.message.chat.id, text=text)
    asyncio.create_task(
        remove_message(chat_id=data.chat.id, message_id=data.message_id, delay=5)
    )


@lockСontrolHandlerRouter.callback_query(
    F.data == LockControlMenuButtons.BotUnlocking.name,
    F.from_user.id.in_(config.tg_bot.admin_ids),
)
async def unblock_bot(callback: CallbackQuery, bot: Bot) -> None:
    callback.answer()
    if callback.message == None:
        return

    controller = BotAccessController()
    result = await controller.unlock()
    text: str = ""
    if not result:
        text = "Разлокировка бота не удалась"
    text = "Бот разблокирован"
    data = await bot.send_message(chat_id=callback.message.chat.id, text=text)
    asyncio.create_task(
        remove_message(chat_id=data.chat.id, message_id=data.message_id, delay=5)
    )
