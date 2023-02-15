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


# обрабатываем команды /start /help
@dp.message_handler(commands=['start', 'help'])
async def start_message(message: types.Message):
    await dp.bot.send_message(
        message.chat.id,
        MESSAGES['start'].format(message.from_user.username),
        reply_markup=set_link_keyboard
    )
    # добавляем айди пользователя в user_id
    try:
        with open('data/users_id.txt', 'r+') as file:
            if not str(message.chat.id) in file.read().split('\n'):
                file.seek(0, 2)
                file.write(str(message.chat.id)+'\n')
    except FileNotFoundError:
        with open('data/users_id.txt', 'w+') as file:
            file.write(str(message.chat.id)+'\n')


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
    try:
        with open('data/url.txt', 'w+', encoding='utf-8') as file:
            file.write(data['url'])
    except FileNotFoundError:
        with open('data/url.txt', 'w+', encoding='utf-8') as file:
            file.write(data['url'])
    await state.finish()
    await bot.send_message(message.chat.id, MESSAGES['link_updated'], reply_markup=update_link_keyboard)
