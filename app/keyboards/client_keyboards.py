from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.handlers.handlers_commands import client_commands

palettes = KeyboardButton(f'{client_commands["Палітри_пігментів"]}')
contacts = KeyboardButton(f'{client_commands["Наші_контакти"]}')
basket = KeyboardButton(f'{client_commands["Мій_кошик"]}')
start_menu = ReplyKeyboardMarkup(resize_keyboard=True)
start_menu.add(palettes).add(contacts).add(basket)


def cancel_markup_client():
    cancel_mark = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = KeyboardButton(f'{client_commands["Відмінити_оформлення"]}')
    return cancel_mark.add(cancel_button)


''' BASKET MARKUP '''
basket_menu = ReplyKeyboardMarkup(resize_keyboard=True
                                  )
make_order = KeyboardButton(f'{client_commands["Оформити_замолення"]}')
home = KeyboardButton(f'{client_commands["start"][1]}')

basket_menu.add(make_order).add(home)

