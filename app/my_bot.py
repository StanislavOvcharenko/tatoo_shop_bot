from aiogram.utils import executor
from app.create_bot import dp
from handlers import client, other, admin


async def on_startup(_):
    print('Bot Start')

client.register_handlers_client(dp)
other.register_handlers_other(dp)
admin.register_handler_admin(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
