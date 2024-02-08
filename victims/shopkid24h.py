import random

from .base import Base
from chrome_fingerprints import FingerprintGenerator


class shopkid24h(Base):
    def __init__(self, proxy: str, fp_gen: FingerprintGenerator):
        super().__init__(proxy, fp_gen=fp_gen)

    def run(self):
        self._register()
        self._transaction()

    def _transaction(self):
        card_name = 'viettel'
        serial = self.create_serial()
        pin = self.create_pin()
        amount = random.choice([50000, 100000, 200000, 300000, 500000])
        data = {
            'loaithe': card_name.upper(),
            'menhgia': str(amount),
            'seri': serial,
            'pin': pin
        }

        response = self.request.post('https://shopkid24h.com/assets/ajaxs/NapThe.php', data=data)
        print(response.text)

    def _register(self):
        username = self.create_username()
        password = self.create_password()
        data = {
            'type': 'Register',
            'username': username,
            'password': password,
            'repassword': password
        }

        response = self.request.post('https://shopkid24h.com/assets/ajaxs/Auth.php', data=data)
        print(response.text)


