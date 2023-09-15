from enum import Enum, StrEnum


class CalendarMenuButtons(Enum):
    CalculateMoneyCalendar = 'Расчитать Денежный Календарь'

class CalendarActionMenuButtons(Enum):
    CalendarConfirmData = 'Подтвердить данные'
    CalendarEditData = 'Исправить данные'

class CalendarPagiBtnCallback(StrEnum):
    backward = 'calendar_backward'
    forward = 'calendar_forward'

