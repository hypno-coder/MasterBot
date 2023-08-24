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
    MoneyCodeBtn1: str = "Денежный Код"
    MoneyCalendarBtn1: str = "Денежный Календарь"
    BackToPaidMenu: str = "Назад"

    # Menu MoneyCode
    MoneyCodeBtn2="Расчитать Финкод"

    # Menu MoneyCalendar
    MoneyCalendarBtn2="Расчитать Денежный Календарь"

    # Menu Jantra
    JantraBtn2: str = "Создать Янтру"

    # Main Menu
    Paid: str = "Платные 💰"
    Free: str = "Бесплатные 🆓"

    # Common Buttons
    BackMainMenu: str = "Главное Меню"
    Backward: str = "<<"
    Forward: str = ">>"
    PagiKeyboard: dict[str, str] = field(default_factory=dict)


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
