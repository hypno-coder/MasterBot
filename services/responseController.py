import base64
import random
from asyncio import sleep
from datetime import datetime

import pdfkit
from aiogram.types import Message
from aiogram.types.input_file import BufferedInputFile, FSInputFile

from keyboards.keyboards_generator import Keyboard
from lexicon import (AdminPaidButtons, CalendarLexicon, CodeLexicon,
                     CommonLexicon, DestinyCardLexicon, JantraLexicon,
                     MainMenuButtons, PaidMenuButtons)
from loader import bot
from payment_services.user_data_type import UserDataType
from services import FinCode, get_calendar_dates
from staticfiles import FilePath


class ResponseController:
    ITEMS_PER_ROW = 1

    def __init__(self, user_data: UserDataType) -> None:
        self.min_delay = int(user_data["min_delay"])
        self.max_delay = int(user_data["max_delay"])
        self.chat_id = user_data["chat_id"]
        self.fio = user_data["fio"]
        self.gender = self.date = (
            user_data["gender"] if user_data["gender"] != None else "female"
        )
        self.jantra = user_data["jantra"]
        self.birthday = user_data["birthday"]
        self.service_species = user_data["service_species"]
        self.back_button = (
            PaidMenuButtons.BackToPaidMenu
            if user_data["adminCallback"] == None
            else AdminPaidButtons.BackToAdminPaidMenu
        )
        self.deliver_for = {
            PaidMenuButtons.MoneyCalendar.name: self.__send_money_calendar_response,
            PaidMenuButtons.MoneyCode.name: self.__send_money_code_response,
            PaidMenuButtons.Jantra.name: self.__send_jantra_response,
            PaidMenuButtons.DestinyCard.name: self.__send_destiny_card_response,
        }
        self.date = (
            datetime.fromisoformat(user_data["month"])
            if user_data["month"] != None
            else datetime.now()
        )
        self.destiny_card = user_data["destiny_card"]
        self.sbornik_id: str

    async def launch(self) -> None:
        await self.__send_greeting()
        await self.deliver_for[self.service_species]()
        await self.__send_keyboard()

    async def __send_greeting(self) -> None:
        delay_message = await self.__send_delay_message()
        await self.__remove_mesaage(delay_message)
        await bot.send_message(chat_id=self.chat_id, text=CommonLexicon.divider)
        await bot.send_message(chat_id=self.chat_id, text=f"<i>{self.fio}</i>")

    async def __send_delay_message(self) -> Message:
        return await bot.send_message(
            self.chat_id,
            text=CommonLexicon.pay_success
            + " "
            + CommonLexicon.message_delay
            + f"{round(self.min_delay/60)}-{round(self.max_delay/60)} минут",
            reply_markup=Keyboard.create_inline(
                self.ITEMS_PER_ROW, backButton=self.back_button
            ),
        )

    async def __remove_mesaage(self, message):
        delay_time = random.randint(self.min_delay, self.max_delay)
        await sleep(delay_time)
        try:
            await bot.delete_message(
                chat_id=message.chat.id, message_id=message.message_id
            )

        except Exception as ex:
            print(ex)

    async def __send_money_collection_response(self) -> None:
        sbornik = FSInputFile(FilePath.sbornik.value)
        await bot.send_document(
            self.chat_id,
            sbornik,
            caption="БлагоДарю за покупку. Используйте полученную информацию во благо!",
        )

    async def __send_money_calendar_response(self) -> None:
        if isinstance(self.date, str):
            return
        calendar_doc = FSInputFile(FilePath.money_calendar_pdf.value)
        calendar_nubers: str = get_calendar_dates(self.date)
        calendar_result = "".join(str(num) for num in calendar_nubers)
        await bot.send_message(
            chat_id=self.chat_id, text=f"<i>{PaidMenuButtons.MoneyCalendar.value}</i>"
        )
        await bot.send_document(
            self.chat_id, calendar_doc, caption=CalendarLexicon.document
        )
        await bot.send_message(
            self.chat_id, f"<b>{CalendarLexicon.for_you}</b> {calendar_result}"
        )

    async def __send_money_code_response(self) -> None:
        code_doc = FSInputFile(FilePath.money_code_pdf.value)
        code_video = FSInputFile(FilePath.money_code_video.value)
        fincode = FinCode()
        if self.birthday == None:
            return
        code_result: str = await fincode.calculate(self.birthday)
        await bot.send_message(
            chat_id=self.chat_id, text=f"<i>{PaidMenuButtons.MoneyCode.value}</i>"
        )
        await bot.send_document(self.chat_id, code_doc, caption=CodeLexicon.document)
        await bot.send_message(
            self.chat_id, f"<b>{CodeLexicon.for_you}</b> {code_result}"
        )
        await bot.send_video(self.chat_id, code_video)

    async def __send_jantra_response(self) -> None:
        jantra_doc = FSInputFile(FilePath.jantra_pdf.value)
        if self.jantra == None:
            return
        image = base64.b64decode(self.jantra["image"].encode("ascii"))
        number = self.jantra["number"]
        input_image = BufferedInputFile(image, "jantra.png")
        await bot.send_message(
            chat_id=self.chat_id, text=f"<i>{PaidMenuButtons.Jantra.value}</i>"
        )
        await bot.send_photo(self.chat_id, input_image)
        await bot.send_message(
            self.chat_id, f"<b>{JantraLexicon.lucky_number+str(number)}</b>"
        )
        await bot.send_document(
            self.chat_id, jantra_doc, caption=JantraLexicon.document
        )

    async def __send_destiny_card_response(self) -> None:
        destiny_card_byte = pdfkit.from_string(
            input=self.destiny_card, options={"encoding": "utf-8"}
        )
        if not isinstance(destiny_card_byte, bytes):
            return
        destiny_card_pdf = BufferedInputFile(
            file=destiny_card_byte, filename=f"{self.fio}.pdf"
        )
        await bot.send_message(
            chat_id=self.chat_id, text=f"<i>{PaidMenuButtons.DestinyCard.value}</i>"
        )
        await bot.send_document(
            self.chat_id, destiny_card_pdf, caption=DestinyCardLexicon.document
        )

    async def __send_keyboard(self) -> None:
        await bot.send_message(chat_id=self.chat_id, text=CommonLexicon.divider)
        await bot.send_message(
            self.chat_id,
            text=CommonLexicon.back_menu,
            reply_markup=Keyboard.create_inline(
                self.ITEMS_PER_ROW, backButton=self.back_button
            ),
        )
