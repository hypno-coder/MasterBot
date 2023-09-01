from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from config_data.payment import Payment, load_payment
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode

config: Config = load_config('.env')
payment: Payment = load_payment('.env')

bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')

storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(storage=storage)
