from aiogram.utils import executor
from app.create_bot import dp
from handlers import client, other, admin
from data_base import Base, engine, AllManagers, session, Creator
from app.handlers.admin import managers_id


async def on_startup(_):
    Base.metadata.create_all(engine)
    for i in session.query(AllManagers).all():
        managers_id.append(i.manager_telegram_id)


    print('Bot Start')

client.register_handlers_client(dp)
other.register_handlers_other(dp)
admin.register_handler_admin(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
