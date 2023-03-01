import sqlalchemy.exc
from aiogram.dispatcher.filters import Text

from app.create_bot import bot
from app.keyboards.client_keyboards import start_menu
from app.keyboards.client_keyboards import choice_tattoo_or_permanent
from app.keyboards.admin_keyboards import choose_keyboard
from app.keyboards.inline import tatoo_and_permanent_inline_button, color_or_zone_inline_button

from app.handlers.handlers_commands import client_commands
from app.handlers.admin import managers_id
from app.data_base import AllClients, session, Pigments, Creator

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


async def choice_keyboard_client(message: types.Message):
    await bot.send_message(message.from_user.id, 'Виберіть необхідний розділ', reply_markup=choice_tattoo_or_permanent)

'''
########################################Tattoo########################################
'''
async def tatoo_creators(message: types.Message):
    all_pigments = session.query(Creator).filter_by(direction="Татту").all()
    for item in all_pigments:
        await bot.send_photo(message.from_user.id, item.photo,
                             reply_markup=tatoo_and_permanent_inline_button("Тату-виробник",
                                                                            item.creator_name, item.creator_name))

async def tattoo_colors(callback: types.CallbackQuery):
    colors = []
    callback_data = callback.data.split('_')
    all_color = session.query(Pigments).filter_by(company_creator=callback_data[1]).filter_by(direction="Татту").all()

    for color in all_color:
        if color.zone_or_color not in colors:
            colors.append(color.zone_or_color)
        else:
            continue

    await bot.send_message(callback.from_user.id, f'{"Виберіть колір:"}',
                           reply_markup=color_or_zone_inline_button('Колір', 'Татту', callback_data[1], colors))


async def tattoo_pigments(callback: types.CallbackQuery):
    callback_data = callback.data.split('_')
    all_pigments_query = session.query(Pigments).filter_by(direction=callback_data[1]).filter_by(
        company_creator=callback_data[2],
        zone_or_color=callback_data[3]).all()

    for pigment in all_pigments_query:
        await bot.send_photo(callback.from_user.id, pigment.photo, f'Назва:{pigment.pigment_name}\n'
                                                                   f'Опис:{pigment.description}\n'
                                                                   f'Ціни та обєм:{pigment.volume_and_price}')

'''
########################################Permanent########################################
'''
async def permanent_creators(message: types.Message):
    all_pigments = session.query(Creator).filter_by(direction="Перманент").all()
    for item in all_pigments:
        await bot.send_photo(message.from_user.id, item.photo, reply_markup=tatoo_and_permanent_inline_button(
            "Перманент-выробник",item.creator_name, item.creator_name))


async def permanent_zones(callback: types.CallbackQuery):
    zones = []
    callback_data = callback.data.split('_')
    print(f'data1: {callback_data}')
    all_zones = session.query(Pigments).filter_by(company_creator=callback_data[1]).filter_by(direction="Перманент").all()

    for zone in all_zones:
        if zone.zone_or_color not in zones:
            zones.append(zone.zone_or_color)
        else:
            continue

    await bot.send_message(callback.from_user.id, f'{"Виберіть зону:"}',
                           reply_markup=color_or_zone_inline_button('Зона', 'Перманент', callback_data[1], zones))


async def permanent_pigments(callback: types.CallbackQuery):
    callback_data = callback.data.split('_')
    print(f'data: {callback_data}')
    all_pigments_permanent_query = session.query(Pigments).filter_by(direction=callback_data[1]).filter_by(
        company_creator=callback_data[2],
        zone_or_color=callback_data[3]).all()

    for pigment in all_pigments_permanent_query:
        await bot.send_photo(callback.from_user.id, pigment.photo, f'Назва:{pigment.pigment_name}\n'
                                                                   f'Опис:{pigment.description}\n'
                                                                   f'Ціни та обєм:{pigment.volume_and_price}')



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=client_commands['start'])
    dp.register_message_handler(contacts, commands=client_commands['Наші_контакти'])
    dp.register_message_handler(choice_keyboard_client, commands=client_commands['Палітри_пігментів'])
    dp.register_message_handler(tatoo_creators, commands=client_commands['Татту_пігменти'])
    dp.register_callback_query_handler(tattoo_colors, Text(startswith="Тату-виробник_"))
    dp.register_callback_query_handler(tattoo_pigments, Text(startswith="Колір_"))
    dp.register_message_handler(permanent_creators, commands=client_commands["Пігменти_для_перманенту"])
    dp.register_callback_query_handler(permanent_zones, Text(startswith="Перманент-выробник"))
    dp.register_callback_query_handler(permanent_pigments, Text(startswith="Зона_"))
