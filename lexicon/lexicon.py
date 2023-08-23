from dataclasses import dataclass, field

@dataclass
class BotHandlerText:
    # Common
    free_menu: str = "Меню бесплатных услуг"        
    paid_menu: str = "Меню платных услуг"        
    menu_placeholder: str = "Нажмите кнопку"
    main_menu: str = "Выберете платные или бесплатные функции"
    sub: str = "Спасибо за подписку на канал! 🎉👏🥳"
    remove_command_menu: str = "Кнопка \"Menu\" удалена 🗑"
    cancel_state: str = "Вы прервали диалог с ботом"
    invalid_format_date: str = "Не правильный формат даты"
    user_saver: dict[str, str] = field(default_factory=dict)
    subscriber: dict[str, str] = field(default_factory=dict)

    # Sonnik
    sonnik_conv: dict[str, str] = field(default_factory=dict)
    sonnik_download_message: str = "Загрузка может занять до 5 минут ..."
    sonnik_error_message: str = "Сонник пока не работает, попробуйте позже"
    sonnik_try_another_image: str = "Попробовать другой образ сна :"
    sonnik_wrong_message: str = ' - не подходит. Нужно писать в сooбщении только ОДНО' + ' ' + 'слово кирилицей без каких либо других символов или цифр. Введите образ сна заново:'

    # Money code
    title_money_code: str = "Денежный код"
    description_money_code: str = "Покупка услуги 'Денежный код'"
    fio_for_money_code: str = "Укажите ФИО в формате: \"Фамилия Имя Очество\""
    payload_money_code: str = "Payment money code"
    only_thursday: str = "Денежный Код можно заказать только в Четверг"
    date_for_money_code: str = "Укажите дату рождения в формате 06.08.1987"
    your_code: str = "Ваш код: "


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


