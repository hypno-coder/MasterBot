from enum import Enum

class BotCBData(Enum):
    #Yantra
    Btn1 = 'Callback_Data_Yantra'
    Btn11 = 'Callback_Data_Create_Yantra'
    
    #MoneyCode
    MoneyCodeBtn1 = 'Callback_Data_MoneyCode'

    Btn2 = 'Callback_Data_Sonnik'
    Btn3 = 'Callback_Data_Taro'
    Btn4 = 'Callback_Data_AffirmDay'
    Btn5 = 'Callback_Data_Horoskop'
    Btn6 = 'Callback_Data_MagicBot'
    BackMenu = 'Callback_Data_Back'
    BackMainMenu = 'Callback_Data_BackToMainMenu'
    BackPaidMenu = 'Callback_Data_BackToPaidMenu'

