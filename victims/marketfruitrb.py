import os
import time

from .base import Base
from chrome_fingerprints import FingerprintGenerator
from bs4 import BeautifulSoup


class marketfruitrb(Base):
    # def __init__(self, proxy: str, fp_gen: FingerprintGenerator):
    def __init__(self, proxy: str):
        # super().__init__(proxy, fp_gen=fp_gen)
        super().__init__(proxy, 'd')

        with open(f'{os.getcwd()}\\victims\\js\\marketfruitrb.js', encoding='utf-8') as file:
            self.script = file.read()

    def run(self):
        self.tick_cloudflare_checkbox('https://marketfruitrb.com/reg.html')
        self.driver.change_mode()
        self.register()
        self.transaction()

    def register(self):
        token = self._get_token()
        recaptchav3_token = self.get_invisible_recaptcha_token('https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LdHnSQfAAAAAIzU16oY8f6qJBKEEVqgNqZGOOxu&co=aHR0cHM6Ly9tYXJrZXRmcnVpdHJiLmNvbTo0NDM.&hl=en&v=MHBiAvbtvk5Wb2eTZHoP1dUd&size=invisible&cb=6wono6y0sczz')
        username = self.create_username()
        name = self.create_fullname()
        password = self.create_password()
        data = {
            '_token': token,
            'token': recaptchav3_token,
            'email': username,
            'name': name,
            'password': password,
            'password1': password,
        }
        self.driver.post('https://marketfruitrb.com/reg.html', data=data)
        with open('Test.html', 'w', encoding='utf-8') as file:
            file.write(self.driver.html)

    def transaction(self):
        serial = self.create_serial()
        pin = self.create_pin()
        recaptchav3_token = self.get_invisible_recaptcha_token('https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LdHnSQfAAAAAIzU16oY8f6qJBKEEVqgNqZGOOxu&co=aHR0cHM6Ly9tYXJrZXRmcnVpdHJiLmNvbTo0NDM.&hl=en&v=MHBiAvbtvk5Wb2eTZHoP1dUd&size=invisible&cb=6wono6y0sczz')
        data = {
            'token': recaptchav3_token,
            'type': 'viettel',
            'amount': '500000',
            'serial': serial,
            'code': pin,
        }
        self.driver.post('https://marketfruitrb.com/transaction/index', data=data)
        print(self.driver.html)

    def _get_token(self):
        self.driver.get('https://marketfruitrb.com/reg.html')
        soup = BeautifulSoup(self.driver.html, 'html.parser')

        token = soup.select_one('input[name="_token"]')
        return token['value']
    