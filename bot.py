from config_data.config import load_config


config = load_config('.env')
bot_token: str = config.tg_bot.token
superadmin: list = config.tg_bot.admin_ids

print(bot_token)
print(superadmin)
