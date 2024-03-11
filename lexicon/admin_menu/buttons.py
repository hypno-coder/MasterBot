from enum import Enum


class AdminMenuButtons(Enum):
    BackToAdminMenu = "Назад"
    Mailing = "Рассылка"
    AdminCalculation = "Админ Расчет"
    LockControl = "Контроль доступа"


class LockControlMenuButtons(Enum):
    BotBlocking = "Блокировать Бота"
    BotUnlocking = "Разблокировать Бота"

class AdminPaidMenuButtons(Enum):
    AdminJantra = f"Янтра"
    AdminMoneyCode = f"ФинКод"
    AdminMoneyCalendar = f"Денежный Календарь"
    AdminDestinyCard = f"Карта Судьбы"
    BackToAdminPaidMenu = "Назад"
