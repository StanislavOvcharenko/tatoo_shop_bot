import sqlalchemy.exc

from app.create_bot import bot
from app.keyboards.client_keyboards import start_menu
from app.keyboards.admin_keyboards import choose_keyboard
from app.handlers.handlers_commands import client_commands
from app.handlers.admin import managers_id
from app.data_base import AllClients, session


from aiogram.dispatcher import Dispatcher
from aiogram import types


async def start(message: types.Message):
    if int(message.from_user.id) in managers_id:
        await bot.send_message(message.from_user.id, 'Виберіть клавіатуру', reply_markup=choose_keyboard)
    else:
        await bot.send_message(message.from_user.id, 'Привіт :)', reply_markup=start_menu)
    try:
        client = AllClients(client_telegram_id=message.from_user.id)
        session.add(client)
        session.commit()
    except:
        session.rollback()




async def contacts(message: types.Message):
    await bot.send_message(message.from_user.id, 'Інтернет магазин: ipiccadilly.com\n'
                                                 'Контактні телефони:\n'
                                                 '+38(096) 648-69-85\n'
                                                 '+38(063) 531-10-93\n'
                                                 '+38(095) 220-11-14\n'
                                                 'Час роботи: Кожен день з 9:00 до 20:00'
                           )
    await bot.send_message(message.from_user.id, 'м.Дніпро, Проспект Дмитра Яворницького 52, ТЦ ЦУМ, 1 поверх\n'
                                                 'Телефон магазину в ТЦ ЦУМ: +38(063) 258-69-03\n'
                                                 'Час роботи: Кожен день з 9:00 до 20:00')
    await bot.send_location(message.from_user.id, '48.465292845969934', '35.04569818039999')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=client_commands['start'])
    dp.register_message_handler(contacts, commands=client_commands['Наші_контакти'])

