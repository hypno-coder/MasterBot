from enum import Enum, StrEnum


class CodeMenuButtons(Enum):
    CalculateMoneyCode = 'Расчитать ФинKод'

class CodeActionMenuButtons(Enum):
    CodeConfirmData = 'Подтвердить данные'
    CodeEditData = 'Исправить данные'

class CodePagiBtnCallback(StrEnum):
    backward = 'code_backward'
    forward = 'code_forward'

