from enum import Enum

class ZodiacButtons(Enum):
    aries       = 'Овен ♈️'
    taurus      = 'Телец ♉️'
    gemini      = 'Близнецы ♊️'
    cancer      = 'Рак ♋️'
    leo         = 'Лев ♌️'
    virgo       = 'Дева ♍️'
    libra       = 'Весы ♎️'
    scorpio     = 'Скорпион ♏️'
    sagittarius = 'Стрелец ♐️'
    capricorn   = 'Козерог ♑️'
    aquarius    = 'Водолей ♒️'
    pisces      = 'Рыбы ♓️'

    def __contains__(self, item):
        return item in self.__class__.__members__

class PeriodZodiacButtons(Enum):
    today       = 'сегодня'
    tomorrow    = 'завтра'
    week        = 'неделя'
    month       = 'месяц'
    compatibility = '-=совместимость=-'

UnitedZodiacButtons = Enum(
    'CombinedZodiacButtons', 
    {**{item.name: item.value for item in PeriodZodiacButtons}, 
     **{item.name: item.value for item in ZodiacButtons}}
)
