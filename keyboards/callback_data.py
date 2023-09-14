from enum import Enum

class BotCBData(Enum):
    # Jantra
    JantraBtn1 = 'Callback_Data_Jantra'
    JantraBtn2 = 'Callback_Data_Create_Jantra'
    JantraBtn3 = 'Callback_Data_Confirm_Data_Jantra'
    JantraBtn4 = 'Callback_Data_Fix_Data_Jantra'
    
    # MoneyCode
    MoneyCodeBtn1 = 'Callback_Data_Money_Code'
    MoneyCodeBtn2 = 'Callback_Data_Calculate_Money_Code'
    MoneyCodeBtn3 = 'Callback_Data_Confirm_Data_Code'
    MoneyCodeBtn4 = 'Callback_Data_Fix_Data_Code'

    # Common
    Btn2 = 'Callback_Data_Sonnik'
    Btn3 = 'Callback_Data_Taro'
    Btn4 = 'Callback_Data_AffirmDay'
    Btn5 = 'Callback_Data_Horoskop'
    Btn6 = 'Callback_Data_MagicBot'
    BackMenu = 'Callback_Data_Back'
    BackToMainMenu = 'Callback_Data_BackToMainMenu'
    BackToPaidMenu = 'Callback_Data_BackToPaidMenu'
    BackToFreeMenu = 'Callback_Data_BackToFreeMenu'

