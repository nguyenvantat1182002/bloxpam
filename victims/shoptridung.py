from .base import Base
from chrome_fingerprints import FingerprintGenerator


class shoptridung(Base):
    def __init__(self, proxy: str, fp_gen: FingerprintGenerator):
        super().__init__(proxy, fp_gen=fp_gen)

    def run(self):
        self.register()
        self.transaction()

    def transaction(self):
        pin = self.create_pin()
        serial = self.create_serial()
        data = {
            'type': 'VIETTEL',
            'amount': '500000',
            'code': pin,
            'serial': serial
        }

        response = self.request.post('https://shoptridung.vn/transaction', data=data)
        print(response.json())

    def register(self):
        username = self.create_username()
        password = self.create_password()
        data = {
            'username': username,
            'password': password,
            'password1': password,
        }

        response = self.request.post('https://shoptridung.vn/login/RegisterUser', data=data)
        print(response.json())
