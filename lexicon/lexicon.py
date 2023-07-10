from dataclasses import dataclass, field

@dataclass
class BotHandlerText:
    main_menu: str = "Главное Меню"        
    sub_main_menu: str = "Спасибо за подписку на канал! 🎉👏🥳"
    user_saver: dict[str, str] = field(default_factory=dict)
    subscriber: dict[str, str] = field(default_factory=dict)

    def __init__(self):
        self.subscriber: dict[str, str] = {
            "inline_text": "Вы не подписанны на канал: Мастерская Желаний", 
            "common_text": "Для того, что бы продолжить пользоваться ботом, вы должны подписаться на канал."}
        self.user_saver: dict[str, str] ={
                "text1": "Новый Пользователь!",
                "text2": "Всего пользователей: "
                }
 

BotText = BotHandlerText()


