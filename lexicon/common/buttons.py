from enum import Enum


class CommonMenuButtons:
    payment = "Оплата"


class ActionChooseGenderButtons(Enum):
    Male = "Mужчина"
    Female = "Женщина"

class ActionChoosePaymentButtons(Enum):
    payment_in_russia = "Оплата из России"
    payment_other_countries = "Оплата из других стран"
