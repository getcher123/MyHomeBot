import logging

import os

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.webhook import WebhookRequestHandler

# set up logging
logging.basicConfig(level=logging.INFO)

# create a bot instance
bot = Bot(token=os.environ.get('BOT_TOKEN'))

# create a dispatcher instance
dp = Dispatcher(bot, storage=MemoryStorage())

# create a webhook request handler
webhook_handler = WebhookRequestHandler(os.environ.get('WEBHOOK_URL'))

# register the webhook with the dispatcher
dp.register_webhook(webhook_handler)