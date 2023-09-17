from random import choice
from typing import cast
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import advisor_action_menu_keyboard
from lexicon import AdvisorMenuButtons, AdvisorActionMenuButtons, AdvisorLexicon, ANSWERS 
from config_data import SpamConfig
from states import FSMAdvisor


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
async def answer_to_question(message: Message) -> None:
    if message.text == None or message.from_user == None:
        return

    response = choice(ANSWERS)
    await message.answer(text=response)
    await message.answer(text=AdvisorLexicon.another_question, reply_markup=advisor_action_menu_keyboard)
