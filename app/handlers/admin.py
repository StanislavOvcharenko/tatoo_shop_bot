import os

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext, Dispatcher

from app.handlers.handlers_commands import admin_commands
from app.create_bot import bot
from app.handlers.state_machines import AddManagers, MakeMailing
from app.keyboards.admin_keyboards import manager_keyboard
from app.keyboards.client_keyboards import start_menu
from app.data_base import AllManagers, session, AllClients, DataMailing

managers_id = []


async def start_add_manager(message: types.Message):
    if int(message.from_user.id) == int(os.getenv('SUPER_USER_ID')):
        await AddManagers.last_name.set()
        await message.reply('Введіть прізвище працівника')


# break state machines
async def cancel_admin_handlers(message: types.Message, state: FSMContext):
    if int(message.from_user.id) in managers_id:
        current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


async def add_last_name_manager(message: types.Message, state: FSMContext):
    if int(message.from_user.id) == int(os.getenv('SUPER_USER_ID')):
        async with state.proxy() as data:
            data['last_name'] = message.text
        await AddManagers.next()
        await message.reply('Введіть ID працівника')


async def add_id_manager(message: types.Message, state: FSMContext):
    if int(message.from_user.id) == int(os.getenv('SUPER_USER_ID')):
        async with state.proxy() as data:
            data['manager_id'] = int(message.from_user.id)
        if data['manager_id'] in managers_id:
            await bot.send_message(message.from_user.id, 'Працівник вже в базі')
        else:
            managers_id.append(data['manager_id'])
            new_manager = AllManagers(last_name=data['last_name'], manager_telegram_id=int(data['manager_id']))
            try:
                session.add(new_manager)
                session.commit()
            except:
                pass

        await state.finish()

async def start_make_mailing(message: types.Message):
    if int(message.from_user.id) in managers_id:
        await MakeMailing.photo.set()
        await message.reply('Завантажте фото')

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
        await state.finish()



async def send_client_keyboard(message: types.Message):
    if int(message.from_user.id) in managers_id:
        await bot.send_message(message.from_user.id, 'Клавіатура кліента', reply_markup=start_menu)


async def send_manager_keyboard(message: types.Message):
    if int(message.from_user.id) in managers_id:
        await bot.send_message(message.from_user.id, 'Клавіатура менеджера', reply_markup=manager_keyboard)


def register_handler_admin(dp: Dispatcher):
    # add manager
    dp.register_message_handler(start_add_manager, commands=admin_commands['Додати_працівника'], state=None)
    dp.register_message_handler(cancel_admin_handlers, state="*", commands=admin_commands['Відмінити'])
    dp.register_message_handler(cancel_admin_handlers, Text(equals=admin_commands['Відмінити'], ignore_case=True),
                                state="*")
    dp.register_message_handler(add_last_name_manager, state=AddManagers.last_name)
    dp.register_message_handler(add_id_manager, state=AddManagers.manager_id)
    # make a mailing
    dp.register_message_handler(start_make_mailing, commands=admin_commands['Зробити_розсилку'], state=None)
    dp.register_message_handler(add_mailing_photo,content_types=['photo'], state=MakeMailing.photo)
    dp.register_message_handler(send_mailing, state=MakeMailing.text)
    # send keyboards
    dp.register_message_handler(send_client_keyboard, commands=admin_commands['Клавіатура_клієнт'])
    dp.register_message_handler(send_manager_keyboard, commands=admin_commands['Клавіатура_менеджера'])
