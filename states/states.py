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
    successful_payment = State()

class FSMCalendar(StatesGroup):
    enter_full_name = State()
    enter_date = State()
    payment_calendar = State()
    calculate_calendare_date = State()
    checkout_query_code = State()
    successful_payment = State()

