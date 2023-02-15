
from aiogram.types import BotCommand


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            BotCommand('set_link', 'установить новую ссылку для поиска'),
            BotCommand('cancel', 'отменить действие'),
        ]
    )
