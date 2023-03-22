import os, ast
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext, Dispatcher
from sqlalchemy.exc import IntegrityError

from app.handlers.handlers_commands import admin_commands
from app.create_bot import bot
from app.handlers.state_machines import MakeMailing, AddPigment, AddCreator, UpdatePriceAndVolume
from app.keyboards.admin_keyboards import manager_keyboard, cancel_markup_admin
from app.keyboards.client_keyboards import start_menu
from app.keyboards.inline import delete_creator_markup
from app.data_base import session, AllClients, DataMailing, Pigments, Creator

managers_id_str = os.getenv('MANAGERS_ID')
managers_id = ast.literal_eval(managers_id_str)

direction_pigment = ['Тату', 'Перманент']


async def start_make_mailing(message: types.Message):
    if int(message.from_user.id) in managers_id:
        await MakeMailing.photo.set()
        await message.reply('Завантажте фото', reply_markup=cancel_markup_admin())


# break state machines
async def cancel_admin_handlers(message: types.Message, state: FSMContext):
    if int(message.from_user.id) in managers_id:
        current_state = await state.get_state()
        if current_state is None:
            return
    await state.finish()
    await message.reply('OK', reply_markup=manager_keyboard)


async def add_mailing_photo(message: types.Message, state: FSMContext):
    if int(message.from_user.id) in managers_id:
        async with state.proxy() as data:
            data['photo_id'] = message.photo[0].file_id
        await MakeMailing.next()
        await message.reply("Введіть текст повідомлення")


async def send_mailing(message: types.Message, state: FSMContext):
    if int(message.from_user.id) in managers_id:
        async with state.proxy() as data:
            data['text'] = message.text
            for client_id in session.query(AllClients).all():
                await bot.send_photo(client_id.client_telegram_id, data['photo_id'], data['text'])
        mailing_data = DataMailing(photo_id=data['photo_id'], text=data['text'])
        session.add(mailing_data)
        session.commit()
        await bot.send_message(message.from_user.id, "Повідомлення було відправленно", reply_markup=start_menu)
        await state.finish()


async def start_add_pigment(message: types.message):
    if message.from_user.id in managers_id:
        await AddPigment.photo.set()
        await message.reply('Завантажте фотографію пігменту', reply_markup=cancel_markup_admin())


async def add_photo_pigment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await AddPigment.next()
    await message.reply('Введіть: "Тату" чи "Перманент"')


async def add_pigment_direction(message: types.Message, state: FSMContext):
    if message.text not in direction_pigment:
        await bot.send_message(message.from_user.id, 'Введені не вірні данні\nВведіть: "Тату" чи "Перманент"')
    else:
        async with state.proxy() as data:
            data['direction'] = message.text
        await AddPigment.next()
        await message.reply('Введіть зону для перманенту  чи колір для тату')


async def add_zone_or_color(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['zone_or_color'] = message.text
        await AddPigment.next()
        await message.reply('Введіть назву пігменту')


async def add_pigment_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pigment_name'] = message.text
    await AddPigment.next()
    await message.reply('Введіть опис пігменту')


async def add_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await AddPigment.next()
    await message.reply('Введіть об\'єми та ціни на пігменти. Формат: (об\'єм: Ціна)')


async def add_volume_and_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['volume_and_price'] = message.text
    await AddPigment.next()
    await message.reply('Введіть виробника')


async def add_company_creator(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['company_creator'] = message.text
    try:
        pigment = Pigments(photo=data["photo"], direction=data["direction"], zone_or_color=data["zone_or_color"],
                           company_creator=data["company_creator"], pigment_name=data["pigment_name"],
                           description=data["description"], volume_and_price=data["volume_and_price"])
        session.add(pigment)
        session.commit()
        await bot.send_message(message.from_user.id, 'Пігмент додано', reply_markup=manager_keyboard)
        await state.finish()
    except IntegrityError:
        session.rollback()
        await bot.send_message(message.from_user.id, "Не вірна назва виробника.\n"
                                                     "Введіть вірну назву знов")


async def start_add_creator(message: types.Message):
    if message.from_user.id in managers_id:
        await AddCreator.direction.set()
        await message.reply('Введіть призначення пігменту("Тату" чи "Перманент")', reply_markup=cancel_markup_admin())


async def add_creator_direction(message: types.Message, state: FSMContext):
    if message.text not in direction_pigment:
        await bot.send_message(message.from_user.id, 'Введені не вірні данні.\n'
                                                     'Введіть: "Тату" чи "Перманент"')
    else:
        async with state.proxy() as data:
            data['direction'] = message.text
        await AddCreator.next()
        await message.reply('Введіть назву виробника\n'
                            'Назву Англійською!!!!!!')


async def add_creator_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    try:
        creator = Creator(direction=data['direction'], creator_name=data['name'])
        session.add(creator)
        session.commit()
        await bot.send_message(message.from_user.id, 'Виробника додано', reply_markup=manager_keyboard)
        await state.finish()
    except IntegrityError:
        session.rollback()
        await bot.send_message(message.from_user.id, 'Назва виробника зайнята. Введіть іншу назву')


async def send_client_keyboard(message: types.Message):
    if int(message.from_user.id) in managers_id:
        await bot.send_message(message.from_user.id, 'Клавіатура кліента', reply_markup=start_menu)


async def send_manager_keyboard(message: types.Message):
    if int(message.from_user.id) in managers_id:
        await bot.send_message(message.from_user.id, 'Клавіатура менеджера', reply_markup=manager_keyboard)


'''################### Delete Creator ###################'''


async def all_creators(message: types.Message):
    if int(message.from_user.id) in managers_id:
        await bot.send_message(message.from_user.id, 'Виберіть виробника', reply_markup=delete_creator_markup())


async def delete_creator(callback: types.CallbackQuery):
    callback_data = callback.data.split('_')
    creator = session.query(Creator).filter_by(creator_name=callback_data[1]).first()
    session.delete(creator)
    session.commit()
    await callback.answer(text="Виробника видалено")


async def start_update_price_and_volume_pigment(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id in managers_id:
        callback_data = callback.data.split('_')
        async with state.proxy() as data:
            data['pigment_id'] = callback_data[1]
        await UpdatePriceAndVolume.new_price_and_volume.set()
        await bot.send_message(callback.from_user.id, 'Введіть нову ціну та об\'єм', reply_markup=cancel_markup_admin())


async def set_new_price_and_volume(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            pigment = session.query(Pigments).filter_by(id=data['pigment_id']).first()
            pigment.volume_and_price = message.text
            session.commit()
        await message.reply(text='Зміни зроблені', reply_markup=start_menu)
    except AttributeError:
        await bot.send_message(message.from_user.id, 'Такого пігменту вже не існує', reply_markup=start_menu)
    finally:
        await state.finish()


def register_handler_admin(dp: Dispatcher):
    # make a mailing
    dp.register_message_handler(start_make_mailing, Text(startswith=admin_commands['Зробити_розсилку']), state=None)
    # cancel handler
    dp.register_message_handler(cancel_admin_handlers, state="*", commands=admin_commands['Відмінити'])
    dp.register_message_handler(cancel_admin_handlers, Text(equals=admin_commands['Відмінити'], ignore_case=True),
                                state="*")
    # and cansel handler
    dp.register_message_handler(add_mailing_photo, content_types=['photo'], state=MakeMailing.photo)
    dp.register_message_handler(send_mailing, state=MakeMailing.text)
    # add pigment
    dp.register_message_handler(start_add_pigment, Text(startswith=admin_commands['Додати_пігмент']), state=None)
    dp.register_message_handler(add_photo_pigment, content_types=['photo'], state=AddPigment.photo)
    dp.register_message_handler(add_pigment_direction, state=AddPigment.direction)
    dp.register_message_handler(add_zone_or_color, state=AddPigment.zone_or_color)
    dp.register_message_handler(add_pigment_name, state=AddPigment.pigment_name)
    dp.register_message_handler(add_description, state=AddPigment.description)
    dp.register_message_handler(add_volume_and_price, state=AddPigment.volume_and_price)
    dp.register_message_handler(add_company_creator, state=AddPigment.company_creator)
    # add Creator
    dp.register_message_handler(start_add_creator, Text(startswith=admin_commands['Додати_виробника']), state=None)
    dp.register_message_handler(add_creator_direction, state=AddCreator.direction)
    dp.register_message_handler(add_creator_name, state=AddCreator.creator_name)
    # send keyboards
    dp.register_message_handler(send_client_keyboard, commands=admin_commands['Клавіатура_клієнта'])
    dp.register_message_handler(send_manager_keyboard, commands=admin_commands['Клавіатура_менеджера'])
    # delete creator
    dp.register_message_handler(all_creators, Text(startswith=admin_commands['Видалити_виробника']))
    dp.register_callback_query_handler(delete_creator, Text(startswith='Видалити-виробника_'))
    dp.register_callback_query_handler(start_update_price_and_volume_pigment, Text(
        startswith='Зміна-ціни_'), state=None)
    dp.register_message_handler(set_new_price_and_volume, state=UpdatePriceAndVolume.new_price_and_volume)
