from aiogram.fsm.state import State, StatesGroup

class FSMSonnik(StatesGroup):
    enter_image = State()
    fill_age = State() 

class FSMCode(StatesGroup):
    calculate_code = State()

