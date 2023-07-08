from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config

config: Config = load_config('.env')
dp: Dispatcher = Dispatcher()
bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
