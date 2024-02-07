from enum import Enum


class AdminMenuButtons(Enum):
    BackToAdminMenu = "Назад"
    Mailing = "Рассылка"
    LockControl = "Контроль доступа"


class LockControlMenuButtons(Enum):
    BotBlocking = "Блокировать Бота"
    BotUnlocking = "Разблокировать Бота"
