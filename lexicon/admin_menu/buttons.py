from enum import Enum


class AdminMenuButtons(Enum):
    BackToAdminMenu = "Назад"
    Mailing = "Рассылка"
    AdminCalculation = "Админ Расчет"
    LockControl = "Контроль доступа"


class LockControlMenuButtons(Enum):
    BotBlocking = "Блокировать Бота"
    BotUnlocking = "Разблокировать Бота"


class AdminPaidButtons(Enum):
    AdminMoenyCollection = 'Денежный сборник'
    AdminJantra = "Янтра"
    AdminMoneyCode = "ФинКод"
    AdminMoneyCalendar = "Денежный Календарь"
    AdminDestinyCard = "Карта Судьбы"
    BackToAdminPaidMenu = "Назад"
