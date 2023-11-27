from enum import Enum 

class MailingActionMenuButtons(Enum):
    StartMailing = 'Начать рассылку'
    MailingEditData = 'Исправить данные'
    
class MailingButtonMenu(Enum):
    MailingAddButton = 'Добавить кнопку'
    MailingUnbutton = 'Без кнопки'

