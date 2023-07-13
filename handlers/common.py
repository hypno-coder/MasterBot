from aiogram import Router
from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import Message
from config_data import SpamConfig  

router: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.common.name}

# Этот хэндлер будет срабатывать на команду "/delmenu"
# и удалять кнопку Menu c командами
@router.message(Command(commands='delmenu'), flags=flags)
async def del_free_menu(message: Message, bot: Bot):
    await bot.delete_my_commands()
    await message.answer(text='Кнопка "Menu" удалена')
