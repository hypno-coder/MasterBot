from enum import Enum

class ZodiacButtons(Enum):
    aries = 'Овен'
    taurus = 'Телец'
    gemini = 'Близнецы'
    cancer = 'Рак'
    leo = 'Лев'
    virgo = 'Дева'
    libra = 'Весы'
    scorpio = 'Скорпион'
    sagittarius = 'Стрелец'
    capricorn = 'Козерог'
    aquarius = 'Водолей'
    pisces = 'Рыбы'

    def __contains__(self, item):
        return item in self.__class__.__members__
