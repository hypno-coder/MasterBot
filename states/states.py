from aiogram.fsm.state import State, StatesGroup

class FSMSonnik(StatesGroup):
    enter_image = State()        # Состояние ожидания ввода имени
    fill_age = State()         # Состояние ожидания ввода возраста
