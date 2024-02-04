import requests
import os
import socket
import subprocess
import random
import string
import capsolver
import time

from DrissionPage import ChromiumPage, ChromiumOptions
from chrome_fingerprints import FingerprintGenerator, ChromeFingerprint
from typing import List, Optional, Callable
from contextlib import closing
from bs4 import BeautifulSoup


FIRST_NAME = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng', 'Huỳnh', 'Vũ', 'Võ', 'Phan', 'Trương', 'Bùi', 'Đặng', 'Đỗ', 'Ngô', 'Hồ', 'Dương', 'Đinh']
MID_NAME = ['Anh', 'Bảo', 'Bình', 'Bửu', 'Công', 'Cường', 'Chí', 'Cao', 'Châu', 'Chiêu', 'Quang', 'Tuấn', 'Huy', 'Văn', 'Thành']


def random_port(host: str = None):
    if not host:
        host = ''
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind((host, 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

class Base:
    _request: requests.Session
    _driver: ChromiumPage
    _glider: subprocess.Popen
    _script: str

    def __init__(self, proxy: str, mode: str = 's', fp_gen: Optional[FingerprintGenerator] = None):
        self._request = None
        self._driver = None
        self._glider = None
        self._script = None

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

                self._driver = ChromiumPage(addr_or_opts=options)

    @property
    def script(self) -> str:
        return self._script
    
    @script.setter
    def script(self, value: str):
        self._script = value

    @property
    def driver(self) -> ChromiumPage:
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

    def tick_cloudflare_checkbox(self):
        try:
            frame = self.driver.get_frame('css:iframe[src*="challenges.cloudflare.com"]', timeout=30)
        except Exception:
            return self.tick_cloudflare_checkbox()

        try:
            while not 'Verify you are human' in frame.inner_html:
                time.sleep(1)

            time.sleep(random.uniform(1.5, 2))
            frame.ele('css:input[type="checkbox"]').check()
        except Exception:
            pass

        self.driver.wait.load_start()
        
        while self.driver.states.is_loading:
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
    
    def create_username(self, length=8):
        username = ''.join(random.choice(string.ascii_letters) for _ in range(length))
        return username

    def create_password(self, length=12):
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
        return password
    
    def create_serial(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(1, 15)])

    def create_pin(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(1, 16)])
    
    def create_fullname(self):
        return f'{random.choice(FIRST_NAME)} {random.choice(MID_NAME)} {random.choice(MID_NAME)}'

    def create_email(self) -> tuple:
        username = self.create_username()
        email = f'{username}@gmail.com'
        return username, email

    def close(self):
        if not self.request is None:
            self.request.close()

        try:
            if not self.driver is None:
                self.driver.quit()
        except Exception as e:
            print(type(e).__name__)

        if not self._glider is None:
            self._glider.kill()

    def _get_user_agent(self) -> str:
        user_agent = None

        if not self.request is None:
            user_agent = self.request.headers['User-Agent']
        elif not self.driver is None:
            user_agent = self.driver.user_agent

        return user_agent
    