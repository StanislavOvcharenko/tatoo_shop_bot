from aiogram.dispatcher.filters import Text
from datetime import date

from app.create_bot import bot
from app.keyboards.client_keyboards import start_menu, cancel_markup_client
from app.keyboards.client_keyboards import basket_menu
from app.keyboards.admin_keyboards import choose_keyboard
from app.keyboards.inline import tatoo_and_permanent_inline_button, color_or_zone_inline_button, delete_item, \
    add_to_basket_markup, choice_tattoo_or_permanent, delete_item_from_basket, choice_any_creator_or_color_or_zone

from app.handlers.handlers_commands import client_commands
from app.handlers.admin import managers_id
from app.handlers.state_machines import MakeOrder
from app.data_base import AllClients, session, Pigments, Orders

from aiogram.dispatcher import Dispatcher, FSMContext
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
                                                 'Час роботи: Пн-Вс з 9:00 до 20:00'
                           )
    await bot.send_message(message.from_user.id, 'м.Дніпро, Проспект Дмитра Яворницького 52, ТЦ ЦУМ, 1 поверх\n'
                                                 'Телефон магазину в ТЦ ЦУМ: +38(063) 258-69-03\n'
                                                 'Час роботи: Пн-Вс з 9:00 до 20:00')
    await bot.send_location(message.from_user.id, '48.465292845969934', '35.04569818039999')


async def choice_keyboard_client(message: types.Message):
    await bot.send_message(message.from_user.id, 'Виберіть необхідний розділ',
                           reply_markup=choice_tattoo_or_permanent())


async def cancel_client_handlers(message: types.Message, state: FSMContext):
    if int(message.from_user.id) in managers_id:
        current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK', reply_markup=start_menu)


'''
########################################Tattoo########################################
'''


async def tatoo_creators(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            reply_markup=tatoo_and_permanent_inline_button(
                                                "Тату-виробник", "Татту"))


async def tattoo_colors(callback: types.CallbackQuery):
    colors = []
    callback_data = callback.data.split('_')
    all_color = session.query(Pigments).filter_by(company_creator=callback_data[1]).filter_by(direction="Татту").all()

    for color in all_color:
        if color.zone_or_color not in colors:
            colors.append(color.zone_or_color)
        else:
            continue
    await callback.answer("Завантажую...")
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                           reply_markup=color_or_zone_inline_button('Колір', 'Татту', callback_data[1], colors))


async def tattoo_pigments(callback: types.CallbackQuery):
    callback_data = callback.data.split('_')
    all_pigments_query = session.query(Pigments).filter_by(direction=callback_data[1]).filter_by(
        company_creator=callback_data[2],
        zone_or_color=callback_data[3]).all()
    await callback.answer("Завантажую...")
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    for pigment in all_pigments_query:
        if callback.from_user.id in managers_id:
            await bot.send_photo(callback.from_user.id, pigment.photo, f'Назва: {pigment.pigment_name}\n'
                                                                       f'Опис: {pigment.description}\n'
                                                                       f'Ціни та обєм: {pigment.volume_and_price}',
                                 reply_markup=delete_item(pigment.pigment_name, pigment.id))
        else:
            await bot.send_photo(callback.from_user.id, pigment.photo, f'Назва:{pigment.pigment_name}\n'
                                                                       f'Опис:{pigment.description}\n'
                                                                       f'Ціни та обєм:{pigment.volume_and_price}',
                                 reply_markup=add_to_basket_markup(pigment.pigment_name, pigment.id))
    await bot.send_message(callback.from_user.id, 'Зробити інший вибір',
                           reply_markup=choice_any_creator_or_color_or_zone('Пігменти-для-перманенту',
                                                                            "Перманент-выробник",
                                                                            callback_data[2]))
'''
########################################Permanent########################################
'''


async def permanent_creators(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        reply_markup=tatoo_and_permanent_inline_button(
                                            "Перманент-выробник", "Перманент"))


async def permanent_zones(callback: types.CallbackQuery):
    zones = []
    callback_data = callback.data.split('_')
    print(f'data1: {callback_data}')
    all_zones = session.query(Pigments).filter_by(company_creator=callback_data[1]).filter_by(
        direction="Перманент").all()
    await callback.answer("Завантажую...")
    for zone in all_zones:
        if zone.zone_or_color not in zones:
            zones.append(zone.zone_or_color)
        else:
            continue

    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                           reply_markup=color_or_zone_inline_button('Зона', 'Перманент', callback_data[1], zones))


async def permanent_pigments(callback: types.CallbackQuery):
    callback_data = callback.data.split('_')
    all_pigments_permanent_query = session.query(Pigments).filter_by(direction=callback_data[1]).filter_by(
        company_creator=callback_data[2],
        zone_or_color=callback_data[3]).all()
    await callback.answer("Завантажую...")
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    for pigment in all_pigments_permanent_query:
        if callback.from_user.id in managers_id:
            await bot.send_photo(callback.from_user.id, pigment.photo, f'Назва: {pigment.pigment_name}\n'
                                                                       f'Опис: {pigment.description}\n'
                                                                       f'Ціни та об\'єм: {pigment.volume_and_price}',
                                 reply_markup=delete_item(pigment.pigment_name, pigment.id))

        else:
            await bot.send_photo(callback.from_user.id, pigment.photo, f'Назва: {pigment.pigment_name}\n'
                                                                       f'Опис: {pigment.description}\n'
                                                                       f'Ціни та об\'єм: {pigment.volume_and_price}',
                                 reply_markup=add_to_basket_markup(pigment.pigment_name, pigment.id))
    await bot.send_message(callback.from_user.id, 'Зробити інший вибір',
                           reply_markup=choice_any_creator_or_color_or_zone('Пігменти-для-перманенту',
                                                                            "Перманент-выробник",
                                                                            callback_data[2]))


async def delete_pigment(callback: types.CallbackQuery):
    callback_data = callback.data.split('_')
    session.query(Pigments).filter(Pigments.id == callback_data[1]).delete()
    session.commit()
    await callback.answer(text=f'Пігмент видалено')


'''################################## Basket ##################################'''


async def add_to_basket(callback: types.CallbackQuery):
    callback_data = callback.data.split('_')
    try:
        order = session.query(Orders).filter_by(client_id=callback.from_user.id).filter_by(order_status=False).first()
        items_list = list(order.items)
        items_list.append(int(callback_data[1]))
        order.items = items_list
        session.commit()
        await callback.answer(text='Підмент додано')
    except AttributeError:
        order = Orders(client_id=callback.from_user.id, items=[int(callback_data[1])])
        session.add(order)
        session.commit()
        await callback.answer(text='Підмент додано')


async def my_basket(message: types.Message):
    try:
        basket = session.query(Orders).filter_by(client_id=message.from_user.id, order_status=False).first()
        a = basket.items[0]
        pigments = session.query(Pigments).all()
        basket_list = list(basket.items)
        await bot.send_message(message.from_user.id, 'Ваше замовлення:', reply_markup=basket_menu)
        for item in basket_list:
            for pigment in pigments:
                if pigment.id == item:
                    await bot.send_photo(message.from_user.id, pigment.photo, f'Назва: {pigment.pigment_name}\n'
                                                                              f'Обьем та ціни: {pigment.volume_and_price}',
                                         reply_markup=delete_item_from_basket(pigment.id))
    except AttributeError:
        await bot.send_message(message.from_user.id, "Ваш кошик пустий🥺\n"
                                                     "За покупками🚀", reply_markup=choice_tattoo_or_permanent())
    except IndexError:
        await bot.send_message(message.from_user.id, "Ваш кошик пустий🥺\n"
                                                     "За покупками🚀", reply_markup=choice_tattoo_or_permanent())

async def delete_from_basket(callback: types.CallbackQuery):
    callback_data = callback.data.split('_')
    basket = session.query(Orders).filter_by(client_id=callback.from_user.id, order_status=False).first()
    basket_list = list(basket.items)
    basket_list.remove(int(callback_data[1]))
    basket.items = basket_list
    session.commit()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


'''################################## Send order ##################################'''


async def start_make_order(message: types.Message):
    await MakeOrder.any_information.set()
    await message.reply('Напишіть кількість та обьеми необхідних пігментів.\n '
                        'Також ви можете вказати инші товари яки вам необхідні або будь-яку іншу інформацию :) ',
                        reply_markup=cancel_markup_client())


async def add_more_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['more_info'] = message.text
    await MakeOrder.next()
    await message.reply(
        'Напишыть данні для відправки вашого замовлення (П.І.П., Номер телефону, Місто доставки, Відділеня НП)')


async def add_delivery_data(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delivery_data'] = message.text
    await MakeOrder.next()
    await message.reply('Напишіть як з вами зв\'язатись бля уточнення і оформлення замовлення.Номер телефону чи '
                        'Інстаграм аккаунт або любий інший спосіб')


async def add_contact_and_send_order(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['how_to_contact'] = message.text

    order = session.query(Orders.items).filter_by(client_id=message.from_user.id, order_status=False).first()
    pigments = session.query(Pigments).all()

    session.query(Orders).filter_by(client_id=message.from_user.id, order_status=False).update({
        "delivery_data": data['delivery_data'], "more_info": data['more_info'],
        "how_to_contact": data['how_to_contact'],
        "order_status": True, "create_date": date.today()})
    session.commit()

    items_in_order = []
    for item in order[0]:
        for pigment in pigments:
            if pigment.id == item:
                items_in_order.append([pigment.pigment_name, pigment.company_creator, pigment.volume_and_price])

    await bot.send_message(managers_id[0], f'Спосіб зв\'язку: {data["how_to_contact"]}\n'
                                           f'Данні доставки: {data["delivery_data"]}\n'
                                           f'Інформація про замовлення: {data["more_info"]}\n'
                                           f'Замовлення: {items_in_order}')

    await bot.send_message(message.from_user.id, 'Замовлення відпраленно менеджеру, з Вами зв\'яжуться в порядку черги',
                           reply_markup=start_menu)
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, Text(startswith=client_commands['start']))
    dp.register_message_handler(contacts, Text(startswith=client_commands['Наші_контакти']))
    dp.register_message_handler(choice_keyboard_client, Text(startswith=client_commands['Палітри_пігментів']))
    dp.register_callback_query_handler(tatoo_creators, Text(startswith="Татту-пігменти_"))
    dp.register_callback_query_handler(tattoo_colors, Text(startswith="Тату-виробник_"))
    dp.register_callback_query_handler(tattoo_pigments, Text(startswith="Колір_"))
    dp.register_callback_query_handler(permanent_creators, Text(startswith='Пігменти-для-перманенту'))
    dp.register_callback_query_handler(permanent_zones, Text(startswith="Перманент-выробник"))
    dp.register_callback_query_handler(permanent_pigments, Text(startswith="Зона_"))
    dp.register_callback_query_handler(delete_pigment, Text(startswith="Видалити-пігмент_"))
    dp.register_callback_query_handler(add_to_basket, Text(startswith="Додати-до-кошика_"))
    dp.register_message_handler(my_basket, Text(startswith=client_commands['Мій_кошик']))
    dp.register_callback_query_handler(delete_from_basket, Text(startswith="Видалити-з-корзини_"))
    # make order
    dp.register_message_handler(start_make_order, Text(startswith=client_commands['Оформити_замолення']), state=None)
    dp.register_message_handler(cancel_client_handlers, state="*", commands=client_commands['Відмінити_оформлення'])
    dp.register_message_handler(cancel_client_handlers, Text(equals=client_commands['Відмінити_оформлення'],
                                                             ignore_case=True),
                                state="*")
    dp.register_message_handler(add_more_info, state=MakeOrder.any_information)
    dp.register_message_handler(add_delivery_data, state=MakeOrder.delivery_data)
    dp.register_message_handler(add_contact_and_send_order, state=MakeOrder.how_to_contact)
