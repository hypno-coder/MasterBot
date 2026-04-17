from enum import Enum

from lexicon import FreeMenuButtons


class MainMenu(Enum):
    BackToMainMenu = "Главное Меню"
#    PaidServices = "Премиум функции 💰"


MainMenuButtons = Enum(
    "MainMenuButtons",
   {
        **{item.name: item.value for item in FreeMenuButtons},
        **{item.name: item.value for item in MainMenu},
    },
)
