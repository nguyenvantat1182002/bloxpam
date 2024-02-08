import hashlib
import json
import numpy as np
import cv2
import pytesseract
import random

from .base import Base
from bs4 import BeautifulSoup


def md5_encode(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()


class xamrobloxnet(Base):
    def __init__(self, proxy: str):
        super().__init__(proxy, 'd')

    def run(self):
        self.tick_cloudflare_checkbox('https://xamroblox.net/')
        self.driver.change_mode()
        self._register()
        self._transaction()

    def _get_captcha(self):
        self.driver.get('https://xamroblox.net/reload-captcha')
        data = json.loads(self.driver.html)
        soup = BeautifulSoup(data['captcha'], 'html.parser')
        captcha_url = soup.select_one('img')['src']
        
        self.driver.get(captcha_url, stream=True)
        image = np.asarray(bytearray(self.driver.raw_data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        preprocessed_image = cv2.medianBlur(image, 3)

        captcha_text: str = pytesseract.image_to_string(preprocessed_image)

        return captcha_text.strip()

    def _transaction(self):
        self.driver.get('https://xamroblox.net/nap-the')

        charge_form = self.driver.ele('css:form[id="form-charge2"]')
        token = charge_form.ele('css:input[name="_token"]').attr('value')
        finger = md5_encode(token)
        captcha_text = self._get_captcha()

        card_name = 'viettel'
        serial = self.create_serial()
        pin = self.create_pin()
        amount = random.choice([50000, 100000, 200000, 300000, 500000])

        data = {
            '_token': token,
            'type': card_name.upper(),
            'amount': str(amount),
            'pin': pin,
            'serial': serial,
            'captcha': captcha_text,
            'finger': finger,
        }
        self.driver.post('https://xamroblox.net/nap-the', data=data)
        print(self.driver.json)

    def _register(self):
        self.driver.get('https://xamroblox.net/')

        register_form = self.driver.ele('css:form[id="formRegister-modal"]')
        token = register_form.ele('css:input[name="_token"]').attr('value')
        username = self.create_username()
        password = self.create_password()
        finger = md5_encode(token)
        data = {
            '_token': token,
            'username': username,
            'password': password,
            'password_confirmation': password,
            'finger': finger,
        }
        self.driver.post('https://xamroblox.net/ajax/register', data=data)
        print(self.driver.json)
