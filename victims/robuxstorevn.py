from .base import Base
from chrome_fingerprints import FingerprintGenerator
from bs4 import BeautifulSoup

import re


class robuxstorevn(Base):
    def __init__(self, proxy: str, fp_gen: FingerprintGenerator):
        super().__init__(proxy, fp_gen=fp_gen)

    def get_items(self):
        response = self.request.get('https://robuxstore.vn/loads/home.php')
        soup = BeautifulSoup(response.text, 'html.parser')

        items = soup.select('div[class="sl-prodli"]')
        result = []

        for item in items:
            try:
                title = item.select_one('span').get_text().strip()
                
                ul = item.select_one('ul')
                li = ul.select('li')
                total_account = li[0].get_text().replace('Số Tài Khoản Hiện Có:', '').strip()
                curr_price = li[1].select_one('button').get_text()
                curr_price = int(curr_price.replace('đ', '').replace(',', ''))

                result.append(f'{title}|{total_account}|{curr_price}')
            except Exception:
                pass

        return result
           

    def get_handler_token(self, url: str):
        response = self.request.get(url)
        html = response.text
        handler_token = re.findall('handler:\s"(.*?)"', html)[-1]
        return handler_token
    
    def register(self):
        handler_token = self.get_handler_token('https://robuxstore.vn/register')
        realname = self.create_fullname()
        username = self.create_username()
        password = self.create_password()

        data = {
            'handler': handler_token,
            'username': username,
            'password': password,
            'repassword': password,
            'realname': realname
        }
        response = self.request.post('https://robuxstore.vn/post/', data=data)
        print(response.text, username, password)

    def transaction(self):
        handler_token = self.get_handler_token('https://robuxstore.vn/')
        type_card = 'viettel'
        amount = 500000
        code = self.create_pin()
        serial = self.create_serial()
        data = {
            'handler': handler_token,
            'type_card': type_card,
            'amount': amount,
            'code': code,
            'serial': serial,
        }
        response = self.request.post('https://robuxstore.vn/post/', data=data)
        print(response.text)

    def run(self):
        self.register()
        self.transaction()
