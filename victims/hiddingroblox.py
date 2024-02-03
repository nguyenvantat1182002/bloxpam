from bs4 import BeautifulSoup
from chrome_fingerprints import FingerprintGenerator
from .base import Base


class hiddingroblox(Base):
    def __init__(self, proxy: str, fp_gen: FingerprintGenerator):
        super().__init__(proxy, fp_gen=fp_gen)

    def run(self):
        pass

    def transaction(self):
        pass

    def register(self):
        pass

    def get_items(self):
        response = self.request.get('https://hiddingroblox.com/')
        soup = BeautifulSoup(response.text, 'html.parser')

        anchors = soup.select('a[href*="/body/random"]')
        result = []
        
        for a in anchors:
            title = a.select_one('h4').get_text().strip()
            total_account = a.select_one('b').get_text().strip()

            spans = a.select('span')
            current_price = spans[-1].get_text().strip()
            if not current_price:
                continue
            current_price = int(current_price.replace('đ', '').replace(',', ''))
            result.append(f'{title}|{total_account}|{current_price}')

        return result

            