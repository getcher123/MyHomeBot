import logging

import os

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.webhook import WebhookRequestHandler
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import (WEBHOOK_URL, WEBHOOK_PATH,
                      WEBAPP_HOST, WEBAPP_PORT)

# set up logging
logging.basicConfig(level=logging.INFO)

# create a bot instance
bot = Bot(token=os.environ.get('BOT_TOKEN'))

# create a dispatcher instance
dp = Dispatcher(bot, storage=MemoryStorage())

# create a webhook request handler
webhook_handler = WebhookRequestHandler(WEBHOOK_URL)

# register the webhook with the dispatcher
dp.register_webhook(webhook_handler)