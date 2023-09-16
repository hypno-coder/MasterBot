from enum import Enum 


class CalendarMenuButtons(Enum):
    CalculateMoneyCalendar = 'Расчитать Денежный Календарь'

class CalendarActionMenuButtons(Enum):
    CalendarConfirmData = 'Подтвердить данные'
    CalendarEditData = 'Исправить данные'

class CalendarPagiBtnCallback():
    backward = 'calendar_backward'
    forward = 'calendar_forward'

