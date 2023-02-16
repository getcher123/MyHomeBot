# импорт типов и состояний из библиотеки aiogram
import asyncio

from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, BadRequest

# импорт модулей бота
from states import Form
from loader import dp, bot
from messages import MESSAGES
from keyboards import set_link_keyboard, update_link_keyboard
from home_parser import MyHomeParser
import os


# обрабатываем команды /start /help
@dp.message_handler(commands=['start', 'help'])
async def start_message(message: types.Message):
    await dp.bot.send_message(
        message.chat.id,
        MESSAGES['start'].format(message.from_user.username),
        reply_markup=set_link_keyboard
    )
    # Add the user ID to the environment variable
    user_ids = os.environ.get('USER_IDS', '').split(',')
    if str(message.chat.id) not in user_ids:
        user_ids.append(str(message.chat.id))
        os.environ['USER_IDS'] = ','.join(user_ids)


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, MESSAGES['cancel'])


@dp.message_handler(commands=['set_link'])
@dp.message_handler(lambda msg: msg.text in ['Задать ссылку для поиска', 'Обновить ссылку для поиска'])
async def set_link_handler(message: types.Message):
    await Form.url.set()
    await bot.send_message(message.chat.id, MESSAGES['set_link'])


@dp.message_handler(state=Form.url)
async def update_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['url'] = message.text
    # Save the URL to an environment variable
    os.environ['URL'] = data['url']
    await state.finish()
    await bot.send_message(message.chat.id, MESSAGES['link_updated'], reply_markup=update_link_keyboard)
