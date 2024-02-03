import os
import time

from .base import Base
from chrome_fingerprints import FingerprintGenerator
from bs4 import BeautifulSoup


class marketfruitrb(Base):
    def __init__(self, proxy: str):
        super().__init__(proxy, 'd')

        with open(f'{os.getcwd()}\\victims\\js\\marketfruitrb.js', encoding='utf-8') as file:
            self.script = file.read()

    def run(self):
        self.driver.get('https://marketfruitrb.com/reg.html')
        self.tick_cloudflare_checkbox()

        self.driver.get('https://marketfruitrb.com/reg.html')
        time.sleep(2)

        username = self.create_username()
        name = self.create_fullname()
        password = self.create_password()
        result = self.driver.run_js_loaded(
            self.script.replace('<method>', 'return await victim.register(arguments[0], arguments[1], arguments[2])'),
            username,
            name,
            password,
            timeout=30
        )

        serial = self.create_serial()
        pin = self.create_pin()
        result = self.driver.run_js_loaded(
            self.script.replace('<method>', 'return await victim.transaction(arguments[0], arguments[1])'),
            serial,
            pin,
            timeout=30
        )
        print(result)


    def register(self):
        token = self._get_token()
        username = self.create_username()
        name = self.create_fullname()
        password = self.create_password()
        data = {
            '_token': token,
            'email': username,
            'name': name,
            'password': password,
            'password1': password,
        }
        response = self.request.post('https://marketfruitrb.com/reg.html', data=data)
        print(response.text)

    def transaction(self):
        serial = self.create_serial()
        pin = self.create_pin()
        data = {
            'type': 'viettel',
            'amount': '500000',
            'serial': serial,
            'code': pin,
        }
        response = self.request.post('https://marketfruitrb.com/transaction/index', data=data)
        print(response.text)

    def _get_token(self):
        response = self.request.get('https://marketfruitrb.com/reg.html')
        soup = BeautifulSoup(response.text, 'html.parser')

        token = soup.select_one('input[name="_token"]')
        return token['value']
    