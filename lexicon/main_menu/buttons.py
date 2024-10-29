from enum import Enum
from lexicon import FreeMenuButtons

class MainMenuButtons(Enum):
    BackToMainMenu = 'Главное Меню'
    FreeServices = 'Бесплатные Услуги 🆓'
    PaidServices = 'Премиум функции 💰'


UnitedMainMenuButtons = Enum(
    'UnitedMainMenuButtons', 
    {**{item.name: item.value for item in MainMenuButtons}, 
     **{item.name: item.value for item in FreeMenuButtons}})
