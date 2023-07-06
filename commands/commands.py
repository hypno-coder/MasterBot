from aiogram import Router
from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import BotCommand

from lexicon.lexicon_ru import LEXICON_COMMANDS_RU

delMenuRouter: Router = Router()

# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
                                command=command,
                                description=description
                          ) for command,
                                description in LEXICON_COMMANDS_RU.items()]
    await bot.set_my_commands(main_menu_commands)


# Этот хэндлер будет срабатывать на команду "/delmenu"
# и удалять кнопку Menu c командами
@delMenuRouter.message(Command(commands='delmenu'))
async def del_main_menu(message: Message, bot: Bot):
    await bot.delete_my_commands()
    await message.answer(text='Кнопка "Menu" удалена')
