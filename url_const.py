from loader import config

# Prod
WEBHOOK_PATH = f"/bot/{config.tg_bot.token}"
WEBHOOK_URL = f"{config.tg_bot.base_url}{WEBHOOK_PATH}"

# Dev
WEBHOOK_NGROK = "https://5d15-85-174-193-51.ngrok-free.app"
WEBHOOK_PATH_DEV = f"/bot/6698538164:AAHKmaLNV_IHegbLu5o_y8HDkEpq77xfhu0"
WEBHOOK_URL_DEV = f"{WEBHOOK_NGROK}{WEBHOOK_PATH_DEV}"
