from .base import Base
from chrome_fingerprints import ChromeFingerprint


class kiwiroblox(Base):
    def __init__(self, proxy: str, fp_gen: ChromeFingerprint):
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
            'pin': pin,
        }

        response = self.request.post('https://kiwiroblox.com/assets/ajaxs/NapThe.php', data=data)
        print(response.text)

    def register(self):
        username, email = self.create_email()
        password = self.create_password()
        recaptcha = self.get_recaptchav2_token('https://kiwiroblox.com/', '6Ld5AU8pAAAAAIH-E1R41q5d5nhztEC7UeFyJNSl')
        data = {
            'type': 'Register',
            'username': username,
            'email': email,
            'password': password,
            'repassword': password,
            'recaptcha': recaptcha
        }

        response = self.request.post('https://kiwiroblox.com/assets/ajaxs/Auth.php', data=data)
        print(response.text)