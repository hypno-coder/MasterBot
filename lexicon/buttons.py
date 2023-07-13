from dataclasses import dataclass

@dataclass
class BotButtonsText:
    # MainMenu
    Btn1: str = "Янтра"
    Btn2: str = "Сонник"
    Btn3: str = "Таро"
    Btn4: str = "Афирмация дня"
    Btn5: str = "Гороскоп"
    Btn6: str = "Магический Бот"
    Btn7: str = "Денежный Код"

    # Common Buttons
    BackMainMenu: str = "Главное Меню"

    # Subscriber Menu
    ChekSub: str = "Проверить подписку 🧙🪄✨"
    Sub: str = "Подписаться"

BotBtnText = BotButtonsText()
