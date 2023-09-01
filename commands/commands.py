from aiogram import Bot
from aiogram.types import BotCommand
from lexicon import COMMANDS


async def set_command_menu(bot: Bot) -> None:
    menu_commands = [BotCommand(
                                command=command,
                                description=description
                          ) for command,
                                description in COMMANDS.items()]
    await bot.set_my_commands(menu_commands)
