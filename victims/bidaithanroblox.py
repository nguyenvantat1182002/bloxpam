import os

from bs4 import BeautifulSoup
from .base import Base


class bidaithanroblox(Base):
    def __init__(self, proxy: str):
        super().__init__(proxy, 'd')

        with open(f'{os.getcwd()}\\victims\\js\\bidaithanroblox.js', encoding='utf-8') as file:
            self.script = file.read()

        self.file_name = 'bidaithanroblox.txt'

    def get_items(self):
        self.get('https://bidaithanroblox.com/')
        self.tick_cloudflare_checkbox()

        soup = BeautifulSoup(self.driver.html, 'html.parser')
        anchors = soup.select('a[href*="/body/random/"]')
        result = []

        for a in anchors[1:]:
            title = a.select_one('h4').get_text().strip()
            total_account = a.select_one('b').get_text().strip()

            spans = a.select('span')
            current_price = spans[-2].get_text().strip()
            current_price = int(current_price.replace('đ', '').replace(',', ''))

            result.append(f'{title}|{total_account}|{current_price}')

        return result
    
    def run(self):
        url = 'https://bidaithanroblox.com/nap-tien.html'

        self.get(url)
        self.tick_cloudflare_checkbox()

        # time.sleep(1)
        # self.get("https://bidaithanroblox.com/")

        username = self.create_username()
        password = self.create_password()
        result = self.driver.run_js_loaded(
            self.script.replace('<method>', f'return await victim.register(arguments[0], arguments[1])'),
            username,
            password,
            timeout=30
        )
        print(result)

        self.get(url)

        serial = self.create_serial()
        pin = self.create_pin()
        # token = self.get_recaptchav2_token(url, '6LfbnCQfAAAAADH94gm1Q_02ntn9vIeOci_P0_gG')
        result = self.driver.run_js_loaded(
            self.script.replace('<method>', f'return await victim.transaction2(arguments[0], arguments[1], arguments[2])'),
            serial,
            pin,
            '',
            timeout=30
        )
        print(result)
