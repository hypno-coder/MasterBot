from dataclasses import dataclass, field

@dataclass
class BotHandlerText:
    sonnik_conv: dict[str, str] = field(default_factory=dict)
    sonnik_download_message: str = 'Загрузка может занять до 5 минут ...'
    sonnik_error_message: str = 'Сонник пока не работает, попробуйте позже'
    sonnik_try_another_image: str = 'Попробовать другой образ сна :'
    sonnik_wrong_message: str = ' - не подходит. Нужно писать в сooбщении только ОДНО' + ' ' + 'слово кирилицей без каких либо других символов или цифр. Введите образ сна заново:'

    def __post_init__(self):
        self.sonnik_conv: dict[str, str] = {
                'start':'Опишите ОДНИМ словом образ вашего сна: '}

BotText = BotHandlerText()
