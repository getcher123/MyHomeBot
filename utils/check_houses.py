import asyncio

from loader import bot
from messages import MESSAGES
from home_parser import MyHomeParser


async def check_new_houses(sleep_time: int):
    while True:
        await asyncio.sleep(sleep_time)
        with open('data/url.txt', 'r') as f:
            url = f.read()
        p = MyHomeParser(url)
        if p.status == 200:
            print(f'status code: {p.status}')
        else:
            print(f'Oh shit... We have a problem, status code: {p.status}')
            continue
        p.get_cards()
        p.get_homes_id()
        p.get_homes_url()
        if p.homes_url and p.homes_id:
            p.save_to_csv()
        else:
            continue
        urls_str = '\n'.join(p.homes_url)
        msg = f"{MESSAGES['house_is_found']}\n\n{urls_str}"
        with open('data/users_id.txt', 'r') as f:
            users = f.readlines()
        for user in users:
            try:
                await bot.send_message(user, msg)
            except Exception as e:
                print(e)
