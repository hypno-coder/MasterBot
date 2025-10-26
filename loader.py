from aiogram import Bot, Dispatcher
from fastapi import FastAPI

from config_data.config import Config, load_config
from config_data.payment import PaymentCredentials, load_payment
from aiogram.fsm.storage.memory import MemoryStorage

config: Config = load_config('.env')
payment: PaymentCredentials = load_payment('.env')

bot: Bot = Bot(token=config.tg_bot.token,parse_mode='HTML')

storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(storage=storage)
app = FastAPI()
