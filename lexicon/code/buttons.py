from enum import Enum 


class CodeMenuButtons(Enum):
    CalculateMoneyCode = 'Расчитать ФинKод'

class CodeActionMenuButtons(Enum):
    CodeConfirmData = 'Подтвердить данные'
    CodeEditData = 'Исправить данные'

class CodePagiBtnCallback():
    backward = 'code_backward'
    forward = 'code_forward'

