from loader import config

# Prod
WEBHOOK_PATH = f"/bot/{config.tg_bot.token}"
WEBHOOK_URL = f"{config.tg_bot.base_url}{WEBHOOK_PATH}"

# Dev
WEBHOOK_NGROK = "https://lgpadj-185-255-176-229.ru.tuna.am"
WEBHOOK_PATH_DEV = f"/bot/6270771768:AAGAAzr3voG8bnSUGIsngRgIBMgtzDux4IA"
WEBHOOK_URL_DEV = f"{WEBHOOK_NGROK}{WEBHOOK_PATH_DEV}"
