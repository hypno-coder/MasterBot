from enum import Enum 


class AdvisorMenuButtons(Enum):
    AskAnAdvisorAQuestion = 'Задать Вопрос'

class AdvisorActionMenuButtons(Enum):
    AskTheAdvisorAgain = 'Спросить еще...'

class AdvisorPagiBtnCallback():
    backward = 'advisor_backward'
    forward = 'advisor_forward'

