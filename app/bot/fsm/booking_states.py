from aiogram.fsm.state import State, StatesGroup


class BookingStates(StatesGroup):
    resource_type = State()
    resource = State()
    date = State()
    time = State()
    confirm = State()