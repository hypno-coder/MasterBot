from enum import Enum, StrEnum


class JantraMenuButtons(Enum):
    CreateJantra = 'Создать Янтру'

class JantraActionMenuButtons(Enum):
    JantraConfirmData = 'Подтвердить данные'
    JantraEditData = 'Исправить данные'

class JantraPagiBtnCallback(StrEnum):
    backward = 'jantra_backward'
    forward = 'jantra_forward'

