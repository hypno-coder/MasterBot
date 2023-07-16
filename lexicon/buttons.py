from dataclasses import dataclass

@dataclass
class BotButtonsText:
    # Free Menu
    Btn2: str = "Сонник"
    Btn3: str = "Таро"
    Btn4: str = "Афирмация дня"
    Btn5: str = "Гороскоп"
    Btn6: str = "Магический Бот"
    
    # Paid Menu
    Btn1: str = "Янтра"
    Btn7: str = "Денежный Код"

    # Main Menu
    Paid: str = "Платные 💰"
    Free: str = "Бесплатные 🆓"

    # Common Buttons
    BackFreeMenu: str = "Главное Меню"

    # Subscriber Menu
    ChekSub: str = "Проверить подписку 🧙🪄✨"
    Sub: str = "Подписаться"

BotBtnText = BotButtonsText()
