from enum import Enum


class DestinyCardMenuButtons(Enum):
    CalculateDestinyCard = "Расчитать Карту Судьбы"


class DestinyCardActionMenuButtons(Enum):
    DestinyCardConfirmData = "Подтвердить данные"
    DestinyCardEditData = "Исправить данные"


class DestinyCardPagiBtnCallback:
    backward = "destiny_card_backward"
    forward = "destiny_card_forward"
