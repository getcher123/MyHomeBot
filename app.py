import asyncio
import os
import logging


from aiogram import executor
from aiogram.utils.executor import start_webhook

from loader import dp, bot
from utils import set_default_commands, check_new_houses
import handlers
from settings import (BOT_TOKEN, HEROKU_APP_NAME,
                          WEBHOOK_URL, WEBHOOK_PATH,
                          WEBAPP_HOST, WEBAPP_PORT)


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    loop = asyncio.get_event_loop()
    loop.create_task(check_new_houses(60))
    await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)
    
async def on_shutdown(dispatcher):
    logging.warning('Bye! Shutting down webhook connection')


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    executor.start_polling(dp, on_startup=on_startup)


