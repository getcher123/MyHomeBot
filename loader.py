import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot_token = os.environ.get('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token, parse_mode='HTML')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())