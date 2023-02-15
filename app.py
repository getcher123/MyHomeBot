import asyncio
import os

from aiogram import executor

from loader import dp
from utils import set_default_commands, check_new_houses
import handlers


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    loop = asyncio.get_event_loop()
    loop.create_task(check_new_houses(60))


if __name__ == '__main__':

# Create data directory if it does not exist
    if not os.path.exists('data'):
        os.makedirs('data')
        with open('data/url.txt', 'w+', encoding='utf-8') as file:
            pass
        with open('data/users_id.txt', 'w+', encoding='utf-8') as file:
            pass
    
    executor.start_polling(dp, on_startup=on_startup)
