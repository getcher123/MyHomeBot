import asyncio
import logging

from aiogram import executor

from loader import dp, bot
from utils import set_default_commands, check_new_houses
from settings import (WEBHOOK_URL, WEBHOOK_PATH,
                      WEBAPP_HOST, WEBAPP_PORT)


async def on_startup(dp):
    logging.info("Starting up...")
    await set_default_commands(dp)
    loop = asyncio.get_event_loop()
    loop.create_task(check_new_houses(60))
    await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Shutting down...')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )