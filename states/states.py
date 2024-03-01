from aiogram.fsm.state import State, StatesGroup


class FSMSonnik(StatesGroup):
    sleeping_pattern = State()
    fill_age = State()


class FSMCode(StatesGroup):
    enter_date = State()
    check_data = State()
    calculate = State()
    checkout_query = State()
    successful_payment = State()


class FSMCalendar(StatesGroup):
    enter_date = State()
    select_month = State()
    check_data = State()
    calculate = State()
    checkout_query = State()
    successful_payment = State()


class FSMDestinyCard(StatesGroup):
    enter_date = State()
    enter_gender = State()
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


class FSMHoroscope(StatesGroup):
    get = State()


class FSMAdvisor(StatesGroup):
    response = State()


class FSMMailing(StatesGroup):
    enter_message = State()
    enter_delay = State()
    enter_image = State()
    add_button = State()
    button_link = State()
    check_data = State()
