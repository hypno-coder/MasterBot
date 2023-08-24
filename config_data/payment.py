from dataclasses import dataclass
from environs import Env

@dataclass
class Price:
    money_code: int
    jantra: int
    money_calendar: int

@dataclass
class Yoomoney:
    token: str
    

@dataclass
class Payment:
    yoomoney: Yoomoney
    currency: str
    price: Price
    

def load_payment(path: str | None) -> Payment:

    env: Env = Env()
    env.read_env(path)

    return Payment(yoomoney=Yoomoney(token=env('PROVIDER_TOKEN')),
                   currency=env('CURRENCY'), 
                   price=Price(
                       money_code=env('MONEY_CODE'), 
                       jantra=env('JANTRA'),
                       money_calendar=env('MONEY_CALENDAR'))
                   )
