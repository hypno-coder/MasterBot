from dataclasses import dataclass, field
from typing import Any

@dataclass
class BotButtonsText:
    # Free Menu
    Btn2: str = "Сонник"
    Btn2_1: str = "Попробовать еще"
    Btn3: str = "Таро"
    Btn4: str = "Афирмация дня"
    Btn5: str = "Гороскоп"
    Btn6: str = "Магический Бот"
    
    # Paid Menu
    JantraBtn1: str = "Янтра"
    MoneyCodeBtn1: str = "ФинКод"
    MoneyCalendarBtn1: str = "Денежный Календарь"
    BackToPaidMenu: str = "Назад"

    # Menu MoneyCode
    MoneyCodeBtn2: str = "Расчитать ФинKод"
    MoneyCodeBtn3: str = "Подтвердить данные"
    MoneyCodeBtn4: str = "Исправить данные"

    # Menu MoneyCalendar
    MoneyCalendarBtn2: str = "Расчитать Денежный Календарь"
    MoneyCalendarBtn3: str = "Подтвердить данные"
    MoneyCalendarBtn4: str = "Исправить данные"


    # Menu Jantra
    JantraBtn2: str = "Создать Янтру"
    JantraBtn3: str = "Подтвердить данные"
    JantraBtn4: str = "Исправить данные"

    # Main Menu
    Paid: str = "Платные 💰"
    Free: str = "Бесплатные 🆓"

    # Common Buttons
    BackMainMenu: str = "Главное Меню"
    PagiKeyboard: dict[str, str] = field(default_factory=dict)
    backward: str = "<<"
    borward: str = ">>"


    # Subscriber Menu
    ChekSub: str = "Проверить подписку 🧙🪄✨"
    Sub: str = "Подписаться"

    def __init__(self):
        self.PagiKeyboard = {'backward': '<<', 'forward': '>>'}


    def find(self, key: str) -> Any:
        if key in self.PagiKeyboard:
            return self.PagiKeyboard[key]
        return False

BotBtnText = BotButtonsText()
