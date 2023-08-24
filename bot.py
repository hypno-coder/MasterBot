import asyncio
import logging

from handlers import mainRouter
from commands import set_command_menu
from middlewares import ThrottlingMiddleware, UserSaverMiddleware, SubscriberMiddleware 
from loader import dp, bot 

logger = logging.getLogger(__name__)

async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    # registr  commands
    await set_command_menu(bot)

    # register middleware
    # dp.message.middleware(ThrottlingMiddleware())
    # dp.message.middleware(UserSaverMiddleware())
    # dp.message.middleware(SubscriberMiddleware())

    # register handlers
    dp.include_router(mainRouter)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    except Exception as ex:
        logging.error(f"Ошибка: {ex}")

    finally:
        await bot.session.close()
        await dp.storage.close()


if __name__ == '__main__':
    asyncio.run(main())
