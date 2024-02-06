import random

from .base import Base
from chrome_fingerprints import FingerprintGenerator


class kidroblox(Base):
    def __init__(self, proxy: str, fp_gen: FingerprintGenerator):
        super().__init__(proxy, fp_gen=fp_gen)

    def run(self):
        self._register()
        self._transaction()

    def _transaction(self):
        card_name = random.choice(['viettel', 'mobifone'])
        price = random.choice([50000, 100000, 200000, 300000, 500000])
        serial = self.create_serial(card_name)
        pin = self.create_pin(card_name)
        data = {
            'loaithe': card_name.upper(),
            'menhgia': str(price),
            'seri': serial,
            'pin': pin,
        }

        response = self.request.post('https://kidroblox.com/assets/ajaxs/NapThe.php', data=data)
        print(response.text)

    def _register(self):
        username = self.create_username()
        password = self.create_password()
        phrase = self.get_recaptchav2_token('https://kidroblox.com/Auth/Register', '6LfTtj0kAAAAAKTERIUfrZd5mSvGDMzwfZrEkxpl')
        data = {
            'type': 'Register',
            'username': username,
            'password': password,
            'phrase': phrase,
            'repassword': password
        }

        response = self.request.post('https://kidroblox.com/assets/ajaxs/Auth.php', data=data)
        print(response.text)
