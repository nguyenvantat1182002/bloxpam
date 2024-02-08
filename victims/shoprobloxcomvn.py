import random

from .base import Base
from chrome_fingerprints import FingerprintGenerator
from bs4 import BeautifulSoup


class shoproblox(Base):
    def __init__(self, proxy: str, fp_gen: FingerprintGenerator):
        super().__init__(proxy, fp_gen=fp_gen)

    def run(self):
        self._register()
        self._transaction()
    
    def _get_token(self, url: str):
        response = self.request.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        token = soup.select_one('input[name="_token"]')['value']
        return token

    def _transaction(self):
        token = self._get_token('https://shoproblox.com.vn/user/money/phone-card/send-card')
        serial = self.create_serial()
        pin = self.create_pin()
        price = random.choice([50000, 100000, 200000, 300000, 500000])
        data = {
            '_token': token,
            'card_network': '1',
            'card_value': str(price),
            'card_seri': serial,
            'card_pin': pin,
            'submit': 'submit',
        }
        response = self.request.post('https://shoproblox.com.vn/user/money/phone-card/send-card', data=data)
        # print(response.text)

    def _register(self):
        token = self._get_token('https://shoproblox.com.vn/auth/register')
        username = self.create_username()
        password = self.create_password()
        data = {
            '_token': token,
            'login_name': username,
            'password': password,
            'password_confirmation': password,
        }
        response = self.request.post('https://shoproblox.com.vn/auth/web-register', data=data)
        # print(response.text)
