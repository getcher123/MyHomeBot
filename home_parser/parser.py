import requests
from bs4 import BeautifulSoup
import sqlite3

class MyHomeParser:

    _headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/104.0.5112.124 YaBrowser/22.9.4.863 Yowser/2.5 Safari/537.36'}

    def __init__(self, url: str):
        self.request = requests.get(url=url, headers=self._headers)
        self.status = self.request.status_code
        self.soup = BeautifulSoup(self.request.text, 'lxml')
        self.cards = []
        self.homes_url = []
        self.homes_id = []
        self.conn = sqlite3.connect('data.db')

    def get_cards(self):
        all_cards = self.soup.select('div[class="statement-card"]')
        self.cards.extend(all_cards)

    def get_homes_url(self):
        cur = self.conn.cursor()
        cur.execute('SELECT url FROM homes')
        old_urls = cur.fetchall()
        for card in self.cards:
            card_href = card.find('a').get('href')[:37]
            if card_href not in old_urls:
                self.homes_url.append(card_href)

    def get_homes_id(self):
        cur = self.conn.cursor()
        cur.execute('SELECT id FROM homes')
        old_ids = cur.fetchall()
        for card in self.cards:
            home_id = int(card.get('data-product-id'))
            if home_id not in old_ids:
                self.homes_id.append(home_id)

    def save_to_db(self):
        cur = self.conn.cursor()
        for url, home_id in zip(self.homes_url, self.homes_id):
            cur.execute('INSERT INTO homes (url, id) VALUES (?, ?)', (url, home_id))
        self.conn.commit()

    def __del__(self):
        self.request.close()
        self.conn.close()
        del self