from .base import Base
from chrome_fingerprints import FingerprintGenerator


class shopkidgm(Base):
    def __init__(self, proxy: str, fp_gen: FingerprintGenerator):
        super().__init__(proxy, fp_gen=fp_gen)

    def run(self):
        self.login()
        self.transaction()

    def transaction(self):
        serial = self.create_serial()
        pin = self.create_pin()
        data = {
            'type': 'VIETTEL',
            'amount': '500000',
            'serial': serial,
            'code': pin
        }
        response = self.request.post('https://shopkidgm.com/transaction', data=data)
        print(response.json())

    def login(self):
        username, password = self.register()
        print(username, password)
        data = {
            'username': username,
            'password': password,
        }
        self.request.post('https://shopkidgm.com/login.html', data=data)

    def register(self):
        name = self.create_username()
        password = self.create_password()
        data = {
            'name': name,
            'password': password,
            'password1': password,
        }
        self.request.post('https://shopkidgm.com/reg.html', data=data)
        return name, password

