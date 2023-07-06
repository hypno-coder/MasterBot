from dataclasses import dataclass

@dataclass
class BotButtonsText:
    # MainMenu
    Btn1: str = "Янтра"
    Btn2: str = "Сонник"
    Btn3: str = "Таро"
    Btn4: str = "Афирмация дня"
    # Common Buttons
    Btn5: str = "Главное Меню"

BotBtnText = BotButtonsText()
