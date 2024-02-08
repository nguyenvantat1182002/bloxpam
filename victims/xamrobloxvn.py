from twocaptcha import TwoCaptcha
from .base import Base
from chrome_fingerprints import FingerprintGenerator

import re
import capsolver
import random


class xamroboxvn(Base):
    _proxy: str

    def __init__(self, proxy: str, fp_gen: FingerprintGenerator):
        self._proxy = proxy
        super().__init__(proxy, fp_gen=fp_gen)

    def run(self):
        if self.register():
            self.gift()
            self.transaction()

    def gift(self):
        response = self.request.get('https://xamroblox.vn/')
        token = re.findall('encodeURIComponent\(\"(.*?)"\)\,', response.text)
        token = token[0]
        data = {
            '': '',
            'token':  token
        }
        response = self.request.post('https://xamroblox.vn/post/', data=data)
        print(response.text)

    def register(self):
        response = self.request.get('https://xamroblox.vn/')
        token = re.findall('encodeURIComponent\(\"(.*?)"\)\,', response.text)
        token = token[1]
        username = self.create_username()
        password = self.create_password()
        # captcha_response = self.captcha_solve('https://xamroblox.vn/')
        # gcaptcha_response = captcha_response['gRecaptchaResponse']
        data = {
            'username': username,
            'password': password,
            'repassword': password,
            # 'g-recaptcha-response': gcaptcha_response,
            # 'h-captcha-response': gcaptcha_response,
            'token': token
        }
        # print(data)
        # headers = {
        #     'User-Agent': captcha_response['userAgent']
        # }
        response = self.request.post('https://xamroblox.vn/post/', data=data)
        data = response.json()
        print(data)
        status = data['status']
        if status == 'success':
            print(username, password)
        return 'success' in status
        

    def captcha_solve(self, url: str):
        solution = capsolver.solve({
            "type": "HCaptchaTaskProxyLess",
            "websiteURL": url,
            "websiteKey": "82921595-b1e2-4328-bc0d-deb80ff86a4f",
            # 'proxy': 'http://' + self._proxy
        })  
        return solution
        # solver = TwoCaptcha('8de9974253e4bc1ca63b136ca5662121')
        # result = solver.turnstile('0x4AAAAAAANAnsvCTrC0wD1Q', url)

        # return result['code']

    def transaction(self):
        response = self.request.get('https://xamroblox.vn/user/recharge')
        token = re.findall('encodeURIComponent\(\"(.*?)"\)\,', response.text)
        token = token[0]
        card_name = random.choice(['viettel', 'mobifone'])
        id_card = self.create_pin(card_name)
        serial = self.create_serial(card_name)
        price = random.choice([50000, 100000, 200000, 300000, 500000])
        # captcha_response = self.captcha_solve('https://xamroblox.vn/user/recharge')
        # gcaptcha_response = captcha_response['gRecaptchaResponse']
        data = {
            'type': card_name.upper(),
            'amount': str(price),
            'code': id_card,
            'serial': serial,
            'token': token,
            # 'g-recaptcha-response': gcaptcha_response,
            # 'h-captcha-response': gcaptcha_response,
        }
        response = self.request.post('https://xamroblox.vn/post/', data=data)
        print(response.json())
