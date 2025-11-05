from dataclasses import dataclass

from environs import Env


@dataclass
class Price:
    money_code: int
    jantra: int
    money_calendar: int
    destiny_card: int


@dataclass
class Robokassa:
    merchant_login: str
    is_test: int
    password_1: str
    password_2: str

@dataclass
class Prodamus:
    secret_key: str
    link_to_form: str


@dataclass
class PaymentCredentials:
    robokassa: Robokassa
    prodamus: Prodamus
    currency: str
    price: Price


def load_payment(path: str | None) -> PaymentCredentials:

    env: Env = Env()
    env.read_env(path)

    return PaymentCredentials(
        robokassa=Robokassa(
            merchant_login=env("MERCHANT_LOGIN"),
            is_test=env("IS_TEST"),
            password_1=env("PASSWORD_1"),
            password_2=env("PASSWORD_2"),
        ),
        prodamus=Prodamus(
            secret_key=env("PROD_SECRET_KEY"),
            link_to_form=env("PROD_LINK_TO_FORM"),
        ),
        currency=env("CURRENCY"),
        price=Price(
            money_code=env("MONEY_CODE"),
            jantra=env("JANTRA"),
            money_calendar=env("MONEY_CALENDAR"),
            destiny_card=env("DESTINY_CARD"),
        ),
    )
