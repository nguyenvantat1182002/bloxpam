import os
import time

from .base import Base


class bidaithanroblox(Base):
    def __init__(self, proxy: str):
        super().__init__(proxy, 'd')

        with open(f'{os.getcwd()}\\victims\\js\\bidaithanroblox.js', encoding='utf-8') as file:
            self.script = file.read()

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
        token = self.get_recaptchav2_token(url, '6LfbnCQfAAAAADH94gm1Q_02ntn9vIeOci_P0_gG')
        result = self.driver.run_js_loaded(
            self.script.replace('<method>', f'return await victim.transaction2(arguments[0], arguments[1], arguments[2])'),
            serial,
            pin,
            token,
            timeout=30
        )
        print(result)
