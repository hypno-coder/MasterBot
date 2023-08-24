from enum import Enum

class BotCBData(Enum):
    # Yantra
    YantraBtn1 = 'Callback_Data_Yantra'
    YantraBtn2 = 'Callback_Data_Create_Yantra'
    
    # MoneyCode
    MoneyCodeBtn1 = 'Callback_Data_MoneyCode'
    MoneyCodeBtn2 = 'Callback_Data_Calculate_MoneyCode'

    # MoneyCalendar
    MoneyCalendarBtn1 = 'Callback_Data_MoneyCalendar'
    MoneyCalendarBtn2 = 'Callback_Data_Calculate_MoneyCalendar'

    # Common
    Btn2 = 'Callback_Data_Sonnik'
    Btn3 = 'Callback_Data_Taro'
    Btn4 = 'Callback_Data_AffirmDay'
    Btn5 = 'Callback_Data_Horoskop'
    Btn6 = 'Callback_Data_MagicBot'
    BackMenu = 'Callback_Data_Back'
    BackToMainMenu = 'Callback_Data_BackToMainMenu'
    BackToPaidMenu = 'Callback_Data_BackToPaidMenu'

