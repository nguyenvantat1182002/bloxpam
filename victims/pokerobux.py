import random
import re

from .base import Base
from chrome_fingerprints import FingerprintGenerator
from bs4 import BeautifulSoup


class pokerobux(Base):
    def __init__(self, proxy: str, fp_gen: FingerprintGenerator):
        super().__init__(proxy, fp_gen=fp_gen)

    def get_items(self):
        response = self.request.get('https://pokerobux.vn/Groups/20')
        soup = BeautifulSoup(response.text, 'html.parser')
        anchors = soup.select('a[href*="https://pokerobux.vn/Accounts/"]')
        titles = {
            '100% Acc Venom Blox Fruits': 'Acc Venom',
            '(UPDATE 20) 100% Acc Mammoth Vĩnh Viễn Blox Fruits': 'Acc Mammoth Vĩnh Viễn',
            '(UPDATE 20) 100% Acc Sound Vĩnh Viễn Blox Fruits': 'Acc Sound Vĩnh Viễn',
            '(ĐẶC BIỆT) ACC BLOX FRUITS HIẾM': 'ACC BLOX FRUITS HIẾM',
            '(ĐẶC BIỆT) ACC BLOX FRUITS HẮC KIẾM YORU': 'HẮC KIẾM YORU',
            '(ĐẶC BIỆT) ACC VUA HẢI TẶC BLOX FRUITS': 'ACC VUA HẢI TẶC',
            '(TRÙM GAME) ACC 30M BOUNTY BLOX FRUITS': 'ACC 30M BOUNTY',
            '(UPDATE MỚI) ACC BLOX FRUITS KITSUNE VĨNH VIỄN': 'KITSUNE VĨNH VIỄN',
            '(UPDATE MỚI) ACC BLOX FRUITS T-REX VĨNH VIỄN': 'T-REX VĨNH VIỄN'
        }
        result = []

        for anchor in anchors:
            title = anchor.select_one('div[class*="font-bold text-md"]')
            total_account = anchor.select_one('b')
            if title is None and total_account is None:
                continue
            title = title.get_text().strip()
            total_account = total_account.get_text().strip()
            price = title.split()[-1].replace('.', '')
            price = int(price) if price.isdecimal() else None
            
            if price is None:
                match titles[title]:
                    case 'Acc Venom':
                        price = 199000
                    case 'Acc Mammoth Vĩnh Viễn':
                        price = 199000
                    case 'Acc Sound Vĩnh Viễn':
                        price = 399000
                    case 'ACC BLOX FRUITS HIẾM':
                        price = 888888
                    case 'HẮC KIẾM YORU':
                        price = 555555
                    case 'ACC VUA HẢI TẶC':
                        price = 999999
                    case 'ACC 30M BOUNTY':
                        price = 1699999
                    case 'KITSUNE VĨNH VIỄN':
                        price = 888999
                    case 'T-REX VĨNH VIỄN':
                        price = 749999
            
            result.append(f'{title}|{total_account}|{price}')

        return result

    def run(self):
        self._register()
        self._transaction()

    def _transaction(self):
        pin = self.create_pin()
        serial = self.create_serial()
        price = random.choice([50000, 100000, 200000, 300000, 500000])
        phrase = self.get_hcaptcha_token('https://pokerobux.vn/', 'b7256a89-6855-48f8-a820-6c115f18ca2e')
        data = {
            'loaithe': 'Viettel',
            'menhgia': str(price),
            'seri': serial,
            'b9fb65fbadcccd0f614a5ec832b3495b': phrase['gRecaptchaResponse'],
            'pin': pin
        }
        response = self.request.post('https://pokerobux.vn/assets/ajaxs/NapThe.php', data=data)
        print(response.text)

    def _register(self):
        phrase = self.get_hcaptcha_token('https://pokerobux.vn/Auth/Register', 'b7256a89-6855-48f8-a820-6c115f18ca2e')
        username = self.create_username()
        password = self.create_password()

        print(username, password)

        data = {
            'type': 'Register',
            'username': username,
            'password': password,
            'phrase': phrase['gRecaptchaResponse'],
            'repassword': password,
        }
        response = self.request.post('https://pokerobux.vn/assets/ajaxs/Auth.php', data=data)
        print(response.text)