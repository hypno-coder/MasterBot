from enum import Enum
from loader import PaymentCredentials

class PaidMenuButtons(Enum):
    Jantra = f'Янтра: {PaymentCredentials.price.jantra}₽'
    MoneyCode = f'ФинКод: {PaymentCredentials.price.money_code}₽'
    MoneyCalendar = f'Денежный Календарь: {PaymentCredentials.price.money_calendar}₽'
    BackToPaidMenu = 'Назад'

