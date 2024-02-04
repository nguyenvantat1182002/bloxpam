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
        # self.register()
        # self.transaction()
        self.get('https://marketfruitrb.com/reg.html')
        self.tick_cloudflare_checkbox()

        # self.get('https://marketfruitrb.com/reg.html')
        # time.sleep(2)

        recaptchav3_token = self.get_invisible_recaptcha_token('https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LdHnSQfAAAAAIzU16oY8f6qJBKEEVqgNqZGOOxu&co=aHR0cHM6Ly9tYXJrZXRmcnVpdHJiLmNvbTo0NDM.&hl=en&v=MHBiAvbtvk5Wb2eTZHoP1dUd&size=invisible&cb=6wono6y0sczz')

        username = self.create_username()
        name = self.create_fullname()
        password = self.create_password()
        result = self.driver.run_js_loaded(
            self.script.replace('<method>', 'return await victim.register(arguments[0], arguments[1], arguments[2], arguments[3])'),
            username,
            name,
            password,
            recaptchav3_token,
            timeout=30
        )

        recaptchav3_token = self.get_invisible_recaptcha_token('https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LdHnSQfAAAAAIzU16oY8f6qJBKEEVqgNqZGOOxu&co=aHR0cHM6Ly9tYXJrZXRmcnVpdHJiLmNvbTo0NDM.&hl=en&v=MHBiAvbtvk5Wb2eTZHoP1dUd&size=invisible&cb=6wono6y0sczz')
        serial = self.create_serial()
        pin = self.create_pin()
        result = self.driver.run_js_loaded(
            self.script.replace('<method>', 'return await victim.transaction(arguments[0], arguments[1], arguments[2])'),
            serial,
            pin,
            recaptchav3_token,
            timeout=30
        )
        print(result)


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
        response = self.request.post('https://marketfruitrb.com/reg.html', data=data)
        # print(response.text)

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
        response = self.request.post('https://marketfruitrb.com/transaction/index', data=data)
        print(response.text)

    def _get_token(self):
        response = self.request.get('https://marketfruitrb.com/reg.html')
        soup = BeautifulSoup(response.text, 'html.parser')

        token = soup.select_one('input[name="_token"]')
        return token['value']
    