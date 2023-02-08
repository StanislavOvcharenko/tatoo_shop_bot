from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

palettes = KeyboardButton('/Палітри_пігментів')
contacts = KeyboardButton('/Наші_контакти')
basket = KeyboardButton('/Мій_кошик')

start_menu = ReplyKeyboardMarkup(resize_keyboard=True)

start_menu.add(palettes).add(contacts).add(basket)

