import os
import random
import time

from chrome_fingerprints import FingerprintGenerator
from bs4 import BeautifulSoup
from .base import Base


class bidaithanroblox(Base):
    def __init__(self, proxy: str, fp_gen: FingerprintGenerator):
        super().__init__(proxy, fp_gen=fp_gen)

        # with open(f'{os.getcwd()}\\victims\\js\\bidaithanroblox.js', encoding='utf-8') as file:
        #     self.script = file.read()

        # self.file_name = 'bidaithanroblox.txt'

    def get_items(self):
        response = self.request.get('https://bidaithanroblox.com/')

        soup = BeautifulSoup(response.text, 'html.parser')
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
    
    def run(self, username: str, password: str):
        return self._register()
        # self._login(username, password)
        # self._transaction()
        # self.tick_cloudflare_checkbox('https://bidaithanroblox.com/nap-tien.html')
        # self.driver.get('https://bidaithanroblox.com/nap-tien.html')
        # self.driver.change_mode()
        # self._register()
        # self._transaction()

        # title = self.driver.title
        # end_time = time.time() + 30
        # while title == self.driver.title:
        #     if time.time() > end_time:
        #         return
        #     time.sleep(1)
        
        # self.driver.change_mode('s')
        # self._register()
        # self._transaction()
        # url = 'https://bidaithanroblox.com/nap-tien.html'

        # self.get(url)
        # self.tick_cloudflare_checkbox()

        # # time.sleep(1)
        # # self.get("https://bidaithanroblox.com/")

        # username = self.create_username()
        # password = self.create_password()
        # result = self.driver.run_js_loaded(
        #     self.script.replace('<method>', f'return await victim.register(arguments[0], arguments[1])'),
        #     username,
        #     password,
        #     timeout=30
        # )
        # print(result)

        # self.get(url)

        # card_name = random.choice(['viettel', 'mobifone'])
        # serial = self.create_serial(card_name)
        # pin = self.create_pin(card_name)
        # # token = self.get_recaptchav2_token(url, '6LfbnCQfAAAAADH94gm1Q_02ntn9vIeOci_P0_gG')
        # result = self.driver.run_js_loaded(
        #     self.script.replace('<method>', f'return await victim.transaction2(arguments[0], arguments[1], arguments[2])'),
        #     card_name.upper(),
        #     serial,
        #     pin,
        #     '',
        #     timeout=30
        # )
        # print(result)
    
    def _login(self, username: str, password: str):
        data = {
            'username': username,
            'password': password
        }
        response = self.request.post('https://bidaithanroblox.com/login/LoginUser', data=data)
        print(response.json())

    def _transaction(self):        
        response = self.request.get('https://bidaithanroblox.com/nap-tien.html')
        token = response.cookies['csrf_cookie_name']
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

        response = self.request.post('https://bidaithanroblox.com/transaction/index', data=data)
        print(response.json())

    def _register(self):
        username = self.create_username()
        password = self.create_password()
        data = {
            'username': username,
            'password': password,
            'password1': password
        }

        response = self.request.post('https://bidaithanroblox.com/login/RegisterUser', data=data)
        data = response.json()

        return [username, password] if data['err'] == 0 else None