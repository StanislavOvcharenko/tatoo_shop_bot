from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class AddManagers(StatesGroup):
    last_name = State()
    manager_id = State()

class MakeMailing(StatesGroup):
    photo = State()
    text = State()


class AddPigment(StatesGroup):
    photo = State()
    direction = State()
    zone_or_color = State()
    company_creator = State()
    pigment_name = State()
    description = State()
    volume_and_price = State()
