from .base import Base
from chrome_fingerprints import FingerprintGenerator


class tuancaythue(Base):
    def __init__(self, proxy: str, fp_gen: FingerprintGenerator):
        super().__init__(proxy, fp_gen=fp_gen)

    def run(self):
        self.register()
        self.transaction()

    def transaction(self):
        serial = self.create_serial()
        pin = self.create_pin()
        data = {
            'loaithe': 'VIETTEL',
            'menhgia': '500000',
            'seri': serial,
            'pin': pin
        }
        response = self.request.post('https://tuancaythue.com/assets/ajaxs/NapThe.php', data=data)
        print(response.text)

    def register(self):
        username = self.create_username()
        password = self.create_password()
        data = {
            'type': 'Register',
            'username': username,
            'password': password,
            'repassword': password
        }
        response = self.request.post('https://tuancaythue.com/assets/ajaxs/Auth.php', data=data)
        print(response.text)