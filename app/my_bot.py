from aiogram.utils import executor
from app.create_bot import dp
from hendlers import client


async def on_startup(_):
    print('Bot Start')

client.register_handlers_client(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
