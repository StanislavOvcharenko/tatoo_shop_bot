from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.data_base import session, Creator, Pigments


def tatoo_and_permanent_inline_button(text, direction):
    all_creators = session.query(Creator).filter_by(direction=direction).all()
    tatoo_inline_markup = InlineKeyboardMarkup(row_width=1)
    for item in all_creators:
        tatoo_inline_button = InlineKeyboardButton(text=f'{item.creator_name}',
                                                   callback_data=f'{text}_{item.creator_name}')
        tatoo_inline_markup.add(tatoo_inline_button)
    return tatoo_inline_markup


def color_or_zone_inline_button(text_command, direction, creator, colors_or_zone):
    inline_markup = InlineKeyboardMarkup(row_width=1)
    for i in colors_or_zone:
        inline_button = InlineKeyboardButton(text=f'{i}', callback_data=f'{text_command}_{direction}_{creator}_{i}')
        inline_markup.add(inline_button)
    return inline_markup


def delete_item(name, item_id):
    delete_inline_markup = InlineKeyboardMarkup(row_width=1)
    delete_inline_button = InlineKeyboardButton(text=f'Видалити: {name}',
                                                callback_data=f'Видалити-пігмент_{item_id}')
    add_to_basket = InlineKeyboardButton(text=f'Додати до кошика: {name}',
                                       callback_data=f'Додати-до-кошика_{item_id}')
    markup = delete_inline_markup.add(delete_inline_button).add(add_to_basket)
    return markup


def delete_creator_markup():
    creators = session.query(Creator).all()
    delete_inline_markup = InlineKeyboardMarkup(row_width=1)
    for creator in creators:
        delete_inline_button = InlineKeyboardButton(text=f'Видалити: {creator.creator_name}',
                                                    callback_data=f'Видалити-виробника_{creator.creator_name}')
        delete_inline_markup.add(delete_inline_button)
    return delete_inline_markup


def add_to_basket_markup(name, pigment_id):
    add_to_basket_mark = InlineKeyboardMarkup(row_width=1)
    add_to_basket_button = InlineKeyboardButton(text=f'Додати до кошика: {name}',
                                                callback_data=f'Додати-до-кошика_{pigment_id}')
    return add_to_basket_mark.add(add_to_basket_button)


def choice_tattoo_or_permanent():
    inline_m = InlineKeyboardMarkup(row_width=1)
    tattoo_button = InlineKeyboardButton(text='Тату Пігменти 👹', callback_data='Татту-пігменти_')
    permanent_button = InlineKeyboardButton(text='Пігменти для перманенту 👄', callback_data='Пігменти-для-перманенту')
    return inline_m.add(tattoo_button).add(permanent_button)


def delete_item_from_basket(pigment_id):
    inline_markup = InlineKeyboardMarkup(row_width=1)
    inline_button = InlineKeyboardButton(text='Видалити з кошика', callback_data=f'Видалити-з-корзини_{pigment_id}')
    return inline_markup.add(inline_button)


def choice_any_creator_or_color_or_zone(direction,text_command, creator):
    choice_markup = InlineKeyboardMarkup(row_width=1)
    choice_creators = InlineKeyboardButton(text='Обрати іншого виробника', callback_data=f'{direction}')
    choice_zone_or_color = InlineKeyboardButton(text=f'Обрати інший колір',
                                                callback_data=f'{text_command}_{creator}')
    return choice_markup.add(choice_creators).add(choice_zone_or_color)


