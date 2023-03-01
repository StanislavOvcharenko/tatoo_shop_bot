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



home_button = ReplyKeyboardMarkup(resize_keyboard=True)

home = KeyboardButton(f'/{client_commands["На_головну_сторінку"]}')

home_button.add(home)



