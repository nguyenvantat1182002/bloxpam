import requests
import os
import socket
import subprocess
import random
import string
import capsolver
import time
import re

from unidecode import unidecode
from DrissionPage import WebPage, ChromiumOptions
from DrissionPage.errors import ElementLostError
from chrome_fingerprints import FingerprintGenerator, ChromeFingerprint
from typing import List, Optional, Callable
from contextlib import closing
from bs4 import BeautifulSoup


FIRST_NAMES = ['Kiều','Sang','Tuyết','Trỉnh','Bắp','Cảnh','Hạ','Triều','Chu','Mã','Lạc','Cao','Trung',
               'Trần','Nguyễn','Võ','Trương','Lai','Lê','Lý','Đinh','Đồng','Mai','Phạm','Vương','Dương','Hoàng','Triệu','Tôn','Phan','Đỗ',
               'Bùi','Đào','Đoàn','Lâm','Phùng', 'Đăng', 'Trương', 'Châu', 'Ngô', 'Huỳnh', 'Trịnh' , 'Ánh', 'Hà', 'Trình', 'Lê', 'Nhựt', 'Cao', 
               'Bành', 'Liên', 'Nguyệt', 'Liễu', 'Lâm Huỳnh']
MID_NAMES = ['Anh', 'Bảo', 'Bình', 'Bửu', 'Công', 'Cường', 'Chí', 'Cao', 'Châu', 
             'Chiêu', 'Quang', 'Tuấn', 'Huy', 'Văn', 'Thành', 'Thị', 'Văn', 'Vô', 'Hữu', 'Hạ', 'Mỹ', 'Tuấn', 'Phi', 'Thành', 'Phục', 
             'Hưng', 'Bình', 'Phương', 'Tuệ', 'Gia', 'Kim' , 'Thanh', 'Nguyệt', 'Ánh', 'Sao', 'Mai', 'Tiểu', 'Nguyên', 'Son', 'Hiền', 'Cầu',
             'Quyển','Ý','Như','Quá', 'Tài', 'Đạt', 'Phúc', 'Lâm', 'Linh', 'Long', 'Quân', 'Nghĩa', 'Phước', 'Tuyền', 'Tiền', 'Phục', 'Châu', 
             'Thanh', 'Thành', 'Chí', 'Trí', 'Tuệ', 'Tăng', 'Ngân', 'Nga', 'Nguyệt', 'Trân', 'Quang', 'Thái', 'Sơn', 'Tiến', 'Mạnh', 'Thảo', 'Phương', 
             'Bách', 'Phong', 'Ngô', 'Nhi', 'Hân', 'Hào', 'Kim', 'Thanh', 'Oanh', 'Hồng', 'Nhung', 'Tiên', 'Hạnh', 'Mẫn', 'Nhi', 'Yến', 
             'Huyền', 'Trâm', 'Anh', 'Nhân', 'Ánh', 'Anh', 'Lì', 'Phúc', 'Sang', 'Tuyết', 'Mai', 'Hoa', 'Chi', 'Toàn', 'Kinh', 'Mỹ', 'Ngọc', 'Hà']


def random_port(host: str = None):
    if not host:
        host = ''
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind((host, 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

class Base:
    _request: requests.Session
    _driver: WebPage
    _glider: subprocess.Popen
    _script: str
    _card_type: dict

    def __init__(self, proxy: str, mode: str = 's', fp_gen: Optional[FingerprintGenerator] = None):
        self._request = None
        self._driver = None
        self._glider = None
        self._script = None
        self._card_type = {
            'viettel': [15, 16],
            'mobifone': [16, 13]
        }

        match mode:
            case 's':
                self._request = requests.Session()
                
                if proxy:
                    self.request.proxies = {
                        'http': f'http://{proxy}',
                        'https': f'http://{proxy}'
                    }
                fingerprint: ChromeFingerprint = fp_gen.get_fingerprint()
                self.request.headers.update({
                    'User-Agent': fingerprint.navigator.user_agent
                })
            case 'd':
                options = ChromiumOptions().auto_port(tmp_path='profiles')
                
                options.set_argument('--force-device-scale-factor', .5)
                options.set_argument('--high-dpi-support', .5)

                options.set_pref('partition.default_zoom_level.x', -3.8017840169239308)
                options.set_pref('credentials_enable_service', False)

                extensions_path = f'{os.getcwd()}\\extensions'
                extension_folders: List[str] = os.listdir(extensions_path)
                for extension_folder in extension_folders:
                    options.add_extension(f'{extensions_path}\\{extension_folder}')                
                
                if proxy:
                    host = '127.0.0.1'
                    port = random_port(host)
                    app_path = f'{os.getcwd()}\\bin\\\glider_0.16.3_windows_amd64\\glider.exe'

                    options.set_proxy(f'http://{host}:{port}')

                    self._glider = subprocess.Popen([app_path, "-listen", f"http://:{port}", "-forward", f"http://{proxy}"])

                self._driver = WebPage(chromium_options=options)

                if proxy:
                    self.driver.session.proxies = {
                        'http': f'http://{proxy}',
                        'https': f'http://{proxy}'
                    }
    
    @property
    def script(self) -> str:
        return self._script
    
    @script.setter
    def script(self, value: str):
        self._script = value

    @property
    def driver(self) -> WebPage:
        return self._driver

    @property
    def request(self) -> requests.Session:
        return self._request
    
    def check2(self, file_name: str, callback: Callable):
        with open(file_name, encoding='utf-8') as file:
            old_data = file.read().splitlines()
            new_data: List[str] = callback()
            data = zip(old_data, new_data)
            total = 0
            for old_info, new_info in data:
                title, total_past_account, price = old_info.split('|')
                _, total_current_account, _ = new_info.split('|')

                total_past_account = int(total_past_account)
                total_current_account = int(total_current_account)
                price = int(price)

                sellable = max(total_past_account, total_current_account) - min(total_past_account, total_current_account)
                total_item_price = price * sellable
                print(title, 'bán được', sellable, 'tổng cộng', total_item_price)

                total += total_item_price

            print('Tổng cộng', total)

    def check(self, file_name: str, callback: Callable):
        with open(file_name, 'a', encoding='utf-8') as file:
            items = callback()
            file.write('\n'.join(items))
    
    def get(self, url: str):
        self.driver.get(url, show_errmsg=True, retry=1)

    def tick_cloudflare_checkbox(self, url: str):
        self.get(url)
        time.sleep(random.uniform(1.5, 2))
        
        title = self.driver.title
        timeout = 10
        
        try:
            frame = self.driver.get_frame('css:iframe[src*="challenges.cloudflare.com"]', timeout=5)
            if not frame:
                return
        except ElementLostError:
            return self.tick_cloudflare_checkbox(url)

        try:
            end_time = time.time() + timeout
            while True:
                if time.time() > end_time:
                    return self.tick_cloudflare_checkbox(url)
                
                if self.driver.title != title:
                    return

                if 'Verify you are human' in frame.inner_html:
                    break

                time.sleep(1)

            time.sleep(random.uniform(1.5, 2))
            frame.ele('css:input[type="checkbox"]').check()
        except Exception:
            return self.tick_cloudflare_checkbox(url)
        
        end_time = time.time() + timeout
        while title == self.driver.title:
            if time.time() > end_time:
                return self.tick_cloudflare_checkbox(url)
            time.sleep(1)

    def get_recaptchav2_token(self, url: str, website_key: str) -> str:
        user_agent = self._get_user_agent()
        solution = capsolver.solve({
            "type": "ReCaptchaV2TaskProxyLess",
            "websiteURL": url,
            "websiteKey": website_key,
            "userAgent": user_agent
        })

        return solution['gRecaptchaResponse']
    
    def get_invisible_recaptcha_token(self, anchor: str):
        content = requests.get(anchor)
        soup = BeautifulSoup(content.text, 'html.parser')
        token = soup.select_one('input[id="recaptcha-token"]')['value']
        result = self.bypass_recaptcha(anchor, token)
        return result

    def bypass_recaptcha(self, anchor: str, token: str):
        v = anchor.split('&v=')[1].split('&')[0]
        k = anchor.split('&k=')[1].split('&')[0]
        co = anchor.split('&co=')[1].split('&')[0]

        data = {
            'v': v,
            'reason': 'q',
            'c': token,
            'k': k,
            'co': co,
            'hl': 'en',
            'size': 'invisible',
            'chr': '1',
            'vh': '1',
            'bg': '5',
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(
                url=f'https://www.google.com/recaptcha/api2/reload?k={k}',
                data=data,
                headers=headers
            )
                
        return response.text.split('["rresp","')[1].split('",')[0]
    
    def _remove_accents(self, input_str: str):
        result_str = unidecode(input_str)
        result_str = result_str.lower()
        result_str = ''.join(c for c in result_str if c.isalnum() or c.isspace())
        return result_str
    
    def _create_username4(self):
        return self._create_username3().title().replace('0', 'k')
    
    def _create_username3(self):
        input_string = f'{random.choice(MID_NAMES)}{random.choice(MID_NAMES)}{random.randint(2001, 2010)}'
        return self._remove_accents(input_string)

    def _create_username2(self):
        input_string = f'{random.choice(FIRST_NAMES)}{random.choice(MID_NAMES)}{random.choice(MID_NAMES)}{random.randint(1000, 10000)}'
        return self._remove_accents(input_string)
    
    def _create_username1(self):
        input_string = f'{random.choice(FIRST_NAMES)}{random.choice(MID_NAMES)}{random.choice(MID_NAMES)}{random.randint(100, 10000)}'
        return re.sub(r'[^a-zA-Z0-9]', '', input_string)
    
    def create_username(self):
        methods = [self._create_username1, self._create_username2, self._create_username3, self._create_username4]
        return random.choice(methods)()
        # return ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(8, 12)))

    def create_password(self, length=12):
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
        return password
    
    def create_serial(self, type_: str = 'viettel'):
        serial = ''.join([str(random.randint(0, 9)) for _ in range(1, self._card_type[type_][0])])
        if type_ == 'viettel':
            serial = '1000' + serial[4:]
        return serial

    def create_pin(self, type_: str = 'viettel'):
        return ''.join([str(random.randint(0, 9)) for _ in range(1, self._card_type[type_][1])])
    
    def create_fullname(self):
        return f'{random.choice(FIRST_NAMES)} {random.choice(MID_NAMES)} {random.choice(MID_NAMES)}'

    def create_email(self) -> tuple:
        username = self.create_username()
        email = f'{username}@gmail.com'
        return username, email

    def close(self):
        if not self.request is None:
            self.request.close()

        if not self.driver is None:
            self.driver.quit()

        if not self._glider is None:
            self._glider.kill()

    def _get_user_agent(self) -> str:
        user_agent = None

        if not self.request is None:
            user_agent = self.request.headers['User-Agent']
        elif not self.driver is None:
            user_agent = self.driver.user_agent

        return user_agent
    