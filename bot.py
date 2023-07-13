import asyncio
import logging

from handlers import common, free_menu 
from commands import set_command_menu
from middlewares import SubscriberMiddleware, UserSaverMiddleware, ThrottlingMiddleware
from loader import dp, bot 

logger = logging.getLogger(__name__)

async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    await set_command_menu(bot)

    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(SubscriberMiddleware())
    dp.message.middleware(UserSaverMiddleware())
    dp.include_router(common.router)
    dp.include_router(free_menu.router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    except Exception as err:
        logging.error(f"Ошибка: {err}")

    finally:
        await bot.session.close()
        await dp.storage.close()


if __name__ == '__main__':
    asyncio.run(main())
