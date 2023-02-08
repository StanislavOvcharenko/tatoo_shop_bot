from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class AddManagers(StatesGroup):
    last_name = State()
    manager_id = State()
