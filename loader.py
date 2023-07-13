from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from aiogram.fsm.storage.memory import MemoryStorage

config: Config = load_config('.env')
bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(storage=storage)
