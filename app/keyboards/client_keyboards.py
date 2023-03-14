from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.handlers.handlers_commands import client_commands

palettes = KeyboardButton(f'/{client_commands["Палітри_пігментів"]}')
contacts = KeyboardButton(f'/{client_commands["Наші_контакти"]}')
basket = KeyboardButton(f'/{client_commands["Мій_кошик"]}')

start_menu = ReplyKeyboardMarkup(resize_keyboard=True)

start_menu.add(palettes).add(contacts).add(basket)

tatoo = KeyboardButton(f'/{client_commands["Татту_пігменти"]}')
permanent = KeyboardButton(f'/{client_commands["Пігменти_для_перманенту"]}')

choice_tattoo_or_permanent = ReplyKeyboardMarkup(resize_keyboard=True)

choice_tattoo_or_permanent.add(tatoo).add(permanent)

''' BASKET MARKUP '''
basket_menu = ReplyKeyboardMarkup(resize_keyboard=True
                                  )
make_order = KeyboardButton(f'/{client_commands["Оформити_замолення"]}')
home = KeyboardButton(f'/{client_commands["start"][1]}')
cancel = KeyboardButton(f'/{client_commands["Відмінити"]}')

basket_menu.add(make_order).add(home).add(cancel)

