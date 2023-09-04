from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove 

from keyboards import paid_menu_keyboard, BotCBData
from lexicon import BotText, BotBtnText 
from config_data import SpamConfig

menuRouter: Router = Router()
flags: dict[str, str] = {"throttling_key": SpamConfig.paid_menu.name}

@menuRouter.message(CommandStart(), flags=flags)
@menuRouter.callback_query(lambda a: a.data == BotCBData.BackToPaidMenu.value, flags=flags)
async def start_paid_menu(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    if isinstance(event, Message):
        await event.answer(text=BotText.paid_menu,
                         reply_markup=paid_menu_keyboard)
        await event.delete()

    elif isinstance(event, CallbackQuery):
        if event.message == None:
            return

        message = event.message
        await message.answer(text=BotText.paid_menu,
                         reply_markup=paid_menu_keyboard)
        await message.delete()

@menuRouter.message(Text(text=BotBtnText.CheckSub), flags=flags)
async def check_sub_paid_menu(message: Message) -> None:
    await message.answer(text=BotText.successful_subscription, 
                         reply_markup=ReplyKeyboardRemove(remove_keyboard=True, selective=True))
    await message.answer(text=BotText.paid_menu,
                         reply_markup=paid_menu_keyboard)



