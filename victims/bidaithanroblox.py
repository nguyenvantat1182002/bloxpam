import random

from bs4 import BeautifulSoup
from .base import Base


class bidaithanroblox(Base):
    def __init__(self, proxy: str):
        super().__init__(proxy, 'd')

    def get_items(self):
        self.tick_cloudflare_checkbox('https://bidaithanroblox.com/')

        soup = BeautifulSoup(self.driver.html, 'html.parser')
        anchors = soup.select('a[href*="/body/random/"]')
        result = []

        for a in anchors[1:]:
            title = a.select_one('h4').get_text().strip()
            total_account = a.select_one('b').get_text().strip()

            spans = a.select('span')
            current_price = spans[-2].get_text().strip()
            current_price = int(current_price.replace('đ', '').replace(',', ''))

            result.append(f'{title}|{total_account}|{current_price}')

        return result
    
    def run(self, username: str = None, password: str = None):
        if username is None and password is None:
            return self._register()
        self._login(username, password)
        self._transaction()
    
    def _login(self, username: str, password: str):
        data = {
            'username': username,
            'password': password
        }
        self.driver.post('https://bidaithanroblox.com/login/LoginUser', data=data)
        print(self.driver.html)

    def _transaction(self):        
        token = self.driver.cookies(as_dict=True)['csrf_cookie_name']
        card_name = random.choice(['viettel', 'mobifone'])
        serial = self.create_serial(card_name)
        pin = self.create_pin(card_name)
        amount = random.choice([50000, 100000, 200000, 300000, 500000])
        data = {
            'type': card_name.upper(),
            'amount': str(amount),
            'serial': serial,
            'code': pin,
            'csrf_test_name': token,
        }

        self.driver.post('https://bidaithanroblox.com/transaction/index', data=data)
        print(self.driver.html)

    def _register(self):
        username = self.create_username()
        password = self.create_password()
        data = {
            'username': username,
            'password': password,
            'password1': password
        }

        self.driver.post('https://bidaithanroblox.com/login/RegisterUser', data=data)
        print(self.driver.html)

        return [username, password] if data['err'] == 0 else None