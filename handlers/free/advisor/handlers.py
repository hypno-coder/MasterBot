from asyncio import sleep
from random import choice, randint
from typing import cast

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import advisor_action_menu_keyboard
from lexicon import AdvisorMenuButtons, AdvisorActionMenuButtons, AdvisorLexicon, ANSWERS 
from config_data import SpamConfig
from states import FSMAdvisor
from utils import remove_message


advisorHandlerRouter: Router = Router()
flags: dict[str, str] = {'throttling_key': SpamConfig.advisor_menu.name}


@advisorHandlerRouter.callback_query(F.data.in_([
   AdvisorMenuButtons.AskAnAdvisorAQuestion.name,
    AdvisorActionMenuButtons.AskTheAdvisorAgain.name]), flags=flags)
async def ask_question(callback: CallbackQuery, state: FSMContext) -> None:
    message = cast(CallbackQuery, callback.message)
    await message.answer(
            text=AdvisorLexicon.ask_question)
    await state.set_state(FSMAdvisor.response)


@advisorHandlerRouter.message(~F.text.startswith('/'), FSMAdvisor.response, flags=flags)
async def answer_to_question(message: Message, bot: Bot) -> None:
    if message.text == None or message.from_user == None:
        return
    data = await bot.send_message(
            chat_id=message.chat.id,
            text=AdvisorLexicon.wait)

    delay = randint(10, 20)
    await sleep(delay)

    await remove_message(chat_id=data.chat.id, message_id=data.message_id, delay=0)

    response = choice(ANSWERS)
    await message.answer(text='===========================')
    await message.answer(text=f'Ответ: {response}')
    await message.answer(text='===========================')
    await message.answer(text=AdvisorLexicon.another_question, reply_markup=advisor_action_menu_keyboard)
