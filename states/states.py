from aiogram.fsm.state import State, StatesGroup

class FSMSonnik(StatesGroup):
    enter_image = State()
    fill_age = State() 

class FSMCode(StatesGroup):
    enter_date = State()
    check_data = State()
    calculate = State()
    checkout_query = State()
    successful_payment = State()

class FSMCalendar(StatesGroup):
    enter_full_name = State()
    enter_date = State()
    check_data = State()
    calculate = State()
    checkout_query = State()
    successful_payment = State()
    
class FSMJantra(StatesGroup):
    enter_date = State()
    check_data = State()
    calculate_data = State()
    checkout_query = State()
    successful_payment = State()


