from aiogram.fsm.state import State, StatesGroup

class FSMSonnik(StatesGroup):
    enter_image = State()
    fill_age = State() 

class FSMCode(StatesGroup):
    enter_full_name = State()
    enter_date = State()
    payment_code = State()
    calculate_code = State()
    checkout_query_code = State()

