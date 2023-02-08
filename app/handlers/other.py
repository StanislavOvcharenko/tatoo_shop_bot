from aiogram import types
from aiogram.dispatcher import Dispatcher
from app.handlers.handlers_commands import other_commands

from app.create_bot import bot


async def my_bot_id(message: types.Message):
    await bot.send_message(message.from_user.id, message.from_user.id)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(my_bot_id, commands=other_commands['Мій_айді'])
