from dataclasses import dataclass, field

@dataclass
class BotHandlerText:
    # Common
    back_menu: str = "Для возврата в меню:"
    help: str = "Для того, что бы прервать диалог с ботом введите /cancel. \nДля того, что бы начать заново введите /start."
    enter_fio: str = "Укажите ФИО в формате: \"Фамилия Имя Очество\" (Фамилия которая дана при рождении)"
    free_menu: str = "Меню бесплатных услуг:"        
    paid_menu: str = "Меню платных услуг:"        
    menu_placeholder: str = "Нажмите кнопку"
    main_menu: str = "Выберете платные или бесплатные функции"
    sub: str = "Спасибо за подписку на канал! 🎉👏🥳"
    remove_command_menu: str = "Кнопка \"Menu\" удалена 🗑"
    cancel_state: str = "Вы прервали диалог с ботом"
    invalid_format_date: str = "Не правильный формат даты"
    user_saver: dict[str, str] = field(default_factory=dict)
    subscriber: dict[str, str] = field(default_factory=dict)
    legal_age: str = "Ваш возраст должен быть от 13 до 80 лет"
    check_data: str = "Проверьте правильность введенных данных: " 
    fio: str = "ФИО: "
    birthday: str = "Дата рождения: "
    selected_action: str = "Выберите, дальнейшее действие: "
    enter_date: str = "Укажите дату рождения в формате 06.08.1987"
    successful_subscription: str = "Поздравляем! Вы успешно подписались на канал Мастерская Желаний, теперь вы можете пользоваться ботом."


    # Sonnik
    sonnik_conv: dict[str, str] = field(default_factory=dict)
    sonnik_download_message: str = "Загрузка может занять до 5 минут ..."
    sonnik_error_message: str = "Сонник пока не работает, попробуйте позже"
    sonnik_try_another_image: str = "Попробовать другой образ сна :"
    sonnik_wrong_message: str = ' - не подходит. Нужно писать в сooбщении только ОДНО' + ' ' + 'слово кирилицей без каких либо других символов или цифр. Введите образ сна заново:'

    # Money code
    money_code_title: str = "Денежный код"
    money_code_payment_description: str = "Покупка услуги: 'Денежный код'"
    money_code_payload: str = "Payment money code"
    money_code_only_thursday: str = "Денежный Код можно заказать только в Четверг"
    money_code_for_you: str = "Ваш код: "
    money_code_document: str = "Это инструкция которая поможет вам разобраться как использовать Денежный Код"
    money_code_description = "Приветствую! Это бот Мастерская Желаний, со временем здесь появится Сонник, Гороскоп, Афирмации, Янтра. А сейчас здесь можно расчитать свой финкод. Для этого нажми кнопку \"Расчитать Финкод\"."

    # Money calendar
    money_calendar_title: str = "Денежный Календарь"
    money_calendar_payment_description: str = "Покупка услуги: Денежный Календарь"
    money_calendar_payload: str = "Payment money calendar"
    money_calendar_for_you: str = "Ваши денежные дни на текущий месяц: \n"
    money_calendar_description: str = "Приветствую! Это бот Мастерская Желаний, со временем здесь появится Сонник, Гороскоп, Афирмации, Янтра. А сейчас здесь можно расчитать свой финкод. Для этого нажми кнопку \"Расчитать Финкод\"."
    money_calendar_document: str = "Это инструкция которая поможет вам разобраться как использовать Денежный Календарь"

    # Jantra
    jantra_title: str = "Янтра"
    jantra_payment_description: str = "Покупка услуги: Янтра"
    jantra_payload: str = "Payment money Jantra"
    jantra_lucky_number: str = "Ваш код удачи: "

    # Utils
    remove_message_error: str = "Попытка удаления уже отредактированooго сooбщения:"
    pay_success: str = "Оплата прошла успешно, "
    message_delay: str = "результат отправлю в течении: "

    def __post_init__(self):
        self.subscriber: dict[str, str] = {
            "inline_text": "Вы не подписанны на канал: Мастерская Желаний", 
            "common_text": "Для того, что бы продолжить пользоваться ботом, вы должны подписаться на канал."}
        self.user_saver: dict[str, str] ={
                "text1": "Новый Пользователь!",
                "text2": "Всего пользователей: "
                }
        self.sonnik_conv: dict[str, str] = {
                "start":"Опишите ОДНИМ словом образ вашего сна: "}

BotText = BotHandlerText()
