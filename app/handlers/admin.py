import os

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext, Dispatcher
from app.handlers.handlers_commands import admin_commands

from app.create_bot import bot
from app.handlers.state_machines import AddManagers


managers_id = []

async def start_add_manager(message: types.Message):
    if int(message.from_user.id) == int(os.getenv('SUPER_USER_ID')):
        await AddManagers.last_name.set()
        await message.reply('Введіть прізвище працівника')


# break state machines
async def cancel_admin_handlers(message: types.Message, state: FSMContext):
    # if int(message.from_user.id) in admins_id:
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
        await bot.send_message(message.from_user.id, f'last name:{data["last_name"]}, manager id: {data["manager_id"]}')
        await state.finish()


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(start_add_manager, commands=admin_commands['Додати_працівника'], state=None)
    dp.register_message_handler(cancel_admin_handlers, state="*", commands=admin_commands['Відмінити'])
    dp.register_message_handler(cancel_admin_handlers, Text(equals=admin_commands['Відмінити'], ignore_case=True),
                                state="*")
    dp.register_message_handler(add_last_name_manager, state=AddManagers.last_name)
    dp.register_message_handler(add_id_manager, state=AddManagers.manager_id)
