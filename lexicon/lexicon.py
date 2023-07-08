from dataclasses import dataclass, field

@dataclass
class BotHandlerText:
    main_menu: str = "Главное Меню"        
    sub_main_menu: str = "Спасибо за подписку на канал! 🎉👏🥳"
    subscriber: dict[str, str] = field(default_factory=dict)

    def __init__(self):
        self.subscriber = {
            "inline_text": "Вы не подписанны на канал: Мастерская Желаний", 
            "common_text": "Для того, что бы продолжить пользоваться ботом, вы должны подписаться на канал."}
 

BotText = BotHandlerText()


