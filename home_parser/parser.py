import requests
from bs4 import BeautifulSoup

import pandas as pd


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

    def get_cards(self):
        all_cards = self.soup.select('div[class="statement-card"]')
        self.cards.extend(all_cards)

    def get_homes_url(self):
        df = pd.read_csv('data/homes.csv')
        old_urls = df['url']
        for card in self.cards:
            card_href = card.find('a').get('href')[:37]
            if card_href not in list(old_urls):
                self.homes_url.append(card_href)

    def get_homes_id(self):
        df = pd.read_csv('data/homes.csv')
        old_ids = df['id']
        for card in self.cards:
            home_id = int(card.get('data-product-id'))
            if home_id not in list(old_ids):
                self.homes_id.append(home_id)

    def save_to_csv(self):
        data_dict = {'url': self.homes_url, 'id': self.homes_id}
        df = pd.DataFrame(data_dict)
        df.to_csv('data/homes.csv', index=False, mode='a', header=False)

    def __del__(self):
        self.request.close()
        del self
