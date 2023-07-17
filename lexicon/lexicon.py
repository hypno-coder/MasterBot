from dataclasses import dataclass, field

@dataclass
class BotHandlerText:
    free_menu: str = "Меню бесплатных услуг"        
    paid_menu: str = "Меню платных услуг"        
    menu_placeholder: str = "Нажмите кнопку"
    main_menu: str = "Тут вы можете выбрать платные или бесплатные услуги"
    sub_free_menu: str = "Спасибо за подписку на канал! 🎉👏🥳"
    remove_command_menu: str = 'Кнопка "Menu" удалена 🗑'
    cancel_state: str = 'Вы прервали диалог с ботом'
    sonnik_conv: dict[str, str] = field(default_factory=dict)
    user_saver: dict[str, str] = field(default_factory=dict)
    subscriber: dict[str, str] = field(default_factory=dict)


    def __post_init__(self):
        self.subscriber: dict[str, str] = {
            "inline_text": "Вы не подписанны на канал: Мастерская Желаний", 
            "common_text": "Для того, что бы продолжить пользоваться ботом, вы должны подписаться на канал."}
        self.user_saver: dict[str, str] ={
                "text1": "Новый Пользователь!",
                "text2": "Всего пользователей: "
                }
        self.sonnik_conv: dict[str, str] = {
                "start":"Опишите ОДНИМ словом образ вашего сна и основную мысль которую вы хотите спросить"}

 

BotText = BotHandlerText()


