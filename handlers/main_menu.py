from aiogram import Router, F
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from keyboards import main_menu_keyboard 
from lexicon import BotBtnText, CommonLexicon, MainMenuButtons
from config_data import SpamConfig

mainMenuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.main_menu.name}

@mainMenuRouter.message(CommandStart(), flags=flags)
@mainMenuRouter.callback_query(F.data == MainMenuButtons.BackToMainMenu.name, flags=flags)
async def start_main_menu(event: Message | CallbackQuery) -> None:
    if isinstance(event, Message):
        await event.answer(text=CommonLexicon.main_menu,
                         reply_markup=main_menu_keyboard)
        await event.delete()

    elif isinstance(event, CallbackQuery):
        if event.message == None:
            return

        await event.answer()
        event = event.message
        await event.edit_text(text=CommonLexicon.main_menu,
                         reply_markup=main_menu_keyboard)


@mainMenuRouter.message(Text(text=BotBtnText.CheckSub), flags=flags)
async def check_sub(message: Message) -> None:
    await message.answer(text=CommonLexicon.successful_subscription, 
                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True, selective=True))
    await message.answer(text=CommonLexicon.paid_menu,
                         reply_markup=main_menu_keyboard)
    await message.delete()




