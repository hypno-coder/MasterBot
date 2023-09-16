from enum import Enum 


class JantraMenuButtons(Enum):
    CreateJantra = 'Создать Янтру'

class JantraActionMenuButtons(Enum):
    JantraConfirmData = 'Подтвердить данные'
    JantraEditData = 'Исправить данные'

class JantraPagiBtnCallback():
    backward = 'jantra_backward'
    forward = 'jantra_forward'

