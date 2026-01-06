from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    func: State = State()
    id: State = State()
