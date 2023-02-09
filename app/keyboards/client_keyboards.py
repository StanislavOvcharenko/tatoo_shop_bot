from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.handlers.handlers_commands import client_commands

palettes = KeyboardButton(f'/{client_commands["Палітри_пігментів"]}')
contacts = KeyboardButton(f'/{client_commands["Наші_контакти"]}')
basket = KeyboardButton(f'/{client_commands["Мій_кошик"]}')

start_menu = ReplyKeyboardMarkup(resize_keyboard=True)

start_menu.add(palettes).add(contacts).add(basket)

