from aiogram.dispatcher.filters.state import StatesGroup, State


class MakeMailing(StatesGroup):
    photo = State()
    text = State()


class AddPigment(StatesGroup):
    photo = State()
    direction = State()
    zone_or_color = State()
    pigment_name = State()
    description = State()
    volume_and_price = State()
    company_creator = State()


class AddCreator(StatesGroup):
    direction = State()
    creator_name = State()


class MakeOrder(StatesGroup):
    any_information = State()
    delivery_data = State()
    how_to_contact = State()


class UpdatePriceAndVolume(StatesGroup):
    new_price_and_volume = State()

