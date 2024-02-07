from enum import Enum, auto 
from .months import months_rus


class CalendarSelectMonthMenuButtons(Enum):
    CurrentMonth = auto() 
    NextMonth = auto()

    @classmethod
    def set_dynamic_values(cls, current, next):
        cls.CurrentMonth._value_ = months_rus[current.month]
        cls.NextMonth._value_ = months_rus[next.month]
        
class CalendarMenuButtons(Enum):
    CalculateMoneyCalendar = 'Расчитать Денежный Календарь'

class CalendarActionMenuButtons(Enum):
    CalendarConfirmData = 'Подтвердить данные'
    CalendarEditData = 'Исправить данные'
    
       
class CalendarPagiBtnCallback():
    backward = 'calendar_backward'
    forward = 'calendar_forward'
