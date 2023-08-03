from dataclasses import dataclass, field

@dataclass
class BotHandlerText:
    free_menu: str = "Меню бесплатных услуг"        
    paid_menu: str = "Меню платных услуг"        
    menu_placeholder: str = "Нажмите кнопку"
    main_menu: str = "Выберете платные или бесплатные функции"
    sub: str = "Спасибо за подписку на канал! 🎉👏🥳"
    remove_command_menu: str = "Кнопка \"Menu\" удалена 🗑"
    cancel_state: str = "Вы прервали диалог с ботом"
    user_saver: dict[str, str] = field(default_factory=dict)
    subscriber: dict[str, str] = field(default_factory=dict)

    # Sonnik
    sonnik_conv: dict[str, str] = field(default_factory=dict)
    sonnik_download_message: str = "Загрузка может занять до 5 минут ..."
    sonnik_error_message: str = "Сонник пока не работает, попробуйте позже"
    sonnik_try_another_image: str = "Попробовать другой образ сна :"
    sonnik_wrong_message: str = ' - не подходит. Нужно писать в сooбщении только ОДНО' + ' ' + 'слово кирилицей без каких либо других символов или цифр. Введите образ сна заново:'


    def __post_init__(self):
        self.subscriber: dict[str, str] = {
            "inline_text": "Вы не подписанны на канал: Мастерская Желаний", 
            "common_text": "Для того, что бы продолжить пользоваться ботом, вы должны подписаться на канал."}
        self.user_saver: dict[str, str] ={
                "text1": "Новый Пользователь!",
                "text2": "Всего пользователей: "
                }
        self.sonnik_conv: dict[str, str] = {
                "start":"Опишите ОДНИМ словом образ вашего сна :"}

 

BotText = BotHandlerText()


