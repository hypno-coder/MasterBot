from enum import Enum
from loader import payment

class PaidMenuButtons(Enum):
    Jantra = f'Янтра: {payment.price.jantra}₽'
    MoneyCode = f'ФинКод: {payment.price.money_code}₽'
    MoneyCalendar = f'Денежный Календарь: {payment.price.money_calendar}₽'
    BackToPaidMenu = 'Назад'

