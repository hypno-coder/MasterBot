from dataclasses import dataclass, field

@dataclass
class BotHandlerText:
    # Sonnik
    sonnik_conv: dict[str, str] = field(default_factory=dict)
    sonnik_download_message: str = 'Загрузка может занять до 5 минут ...'
    sonnik_error_message: str = 'Сонник пока не работает, попробуйте позже'
    sonnik_try_another_image: str = 'Попробовать другой образ сна :'
    sonnik_wrong_message: str = ' - не подходит. Нужно писать в сooбщении только ОДНО' + ' ' + 'слово кирилицей без каких либо других символов или цифр. Введите образ сна заново:'

    # Money code
    money_code_title: str = 'Денежный код'
    money_code_payment_description: str = 'Покупка услуги: "Денежный код"'
    money_code_payload: str = 'Payment money code'
    money_code_only_thursday: str = 'Денежный Код можно заказать только в Четверг'
    money_code_for_you: str = 'Ваш код: '
    money_code_document: str = 'Это инструкция которая поможет вам разобраться как использовать Денежный Код'
    money_code_description = 'Приветствую! Это бот Мастерская Желаний, со временем здесь появится Сонник, Гороскоп, Афирмации, Янтра. А сейчас здесь можно расчитать свой финкод. Для этого нажми кнопку \'Расчитать Финкод\'.'

    # Jantra
    jantra_title: str = 'Янтра'
    jantra_payment_description: str = 'Покупка услуги: Янтра'
    jantra_payload: str = 'Payment money Jantra'
    jantra_lucky_number: str = 'Ваш код удачи: '

    # Utils
    remove_message_error: str = 'Попытка удаления уже отредактированooго сooбщения:'
    pay_success: str = 'Оплата прошла успешно, '
    message_delay: str = 'результат отправлю в течении: '

    def __post_init__(self):
        self.sonnik_conv: dict[str, str] = {
                'start':'Опишите ОДНИМ словом образ вашего сна: '}

BotText = BotHandlerText()
