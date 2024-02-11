from .base import Base
from chrome_fingerprints import FingerprintGenerator


class dichvurobux(Base):
    def __init__(self, proxy: int, fp_gen: FingerprintGenerator):
        super().__init__(proxy, fp_gen=fp_gen)

    def run(self):
        self._register()
        self._transaction()

    def _transaction(self):
        serial = self.create_serial()
        pin = self.create_pin()
        data = {
            'loaithe': 'Viettel',
            'menhgia': '500000',
            'seri': serial,
            'pin': pin
        }
        response = self.request.post('https://dichvurobux.net/assets/ajaxs/NapThe.php', data=data)
        print(response.text)

    def _register(self):
        username = self.create_username()
        password = self.create_password()
        data = {
            'type': 'Register',
            'username': username,
            'password': password,
            'repassword': password,
        }
        response = self.request.post('https://dichvurobux.net/assets/ajaxs/Auth.php', data=data)
        print(response.text)