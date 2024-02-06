from victims import *

# from chrome_fingerprints import FingerprintGenerator


# fp_gen = FingerprintGenerator()

proxy = 'CSkoRcrY:RdMU7ou9@171.250.134.190:6015'
victim = bidaithanroblox(proxy)
victim.run()

# victim.check('bidaithanroblox.txt', victim.get_items)

# victim._register()
# victim.driver.get('https://bidaithanroblox.com/')
# with open('Test.html', 'w', encoding='utf-8') as file:
#     file.write(victim.driver.html)
# victim.run()

# import capsolver
# capsolver.api_key = "CAP-FFE2271E0A6E1961C4FB2BF717C81F0D"


# victim = shoptridung('brZgipEN:OvBNcLMk@171.235.160.120:21001', fp_gen)
# victim.run()

# from DrissionPage import ChromiumPage, ChromiumOptions


# import time


# options = ChromiumOptions().auto_port(tmp_path='profiles')
# options.set_proxy('http://127.0.0.1:4000')
# driver = ChromiumPage(addr_or_opts=options)
# try:
#     driver.get('https://www.facebook.com/', show_errmsg=True, retry=1)
#     time.sleep(4)
# except Exception as e:
#     print(type(e).__name__)

# driver.quit()

# import re
# import random

# from unidecode import unidecode

# FIRST_NAME = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng', 'Huỳnh', 'Vũ', 'Võ', 'Phan', 'Trương', 'Bùi', 'Đặng', 'Đỗ', 'Ngô', 'Hồ', 'Dương', 'Đinh']
# MID_NAME = ['Anh', 'Bảo', 'Bình', 'Bửu', 'Công', 'Cường', 'Chí', 'Cao', 'Châu', 'Chiêu', 'Quang', 'Tuấn', 'Huy', 'Văn', 'Thành']

# def remove_special_characters(input_string):
#     # Sử dụng biểu thức chính quy để chỉ chấp nhận các ký tự chữ cái và chữ số
#     return re.sub(r'[^a-zA-Z0-9]', '', input_string)

# def remove_accents(input_str):
#     # Sử dụng unidecode để chuyển đổi các ký tự có dấu thành dạng không dấu
#     result_str = unidecode(input_str)
    
#     # Chuyển đổi thành chữ thường
#     result_str = result_str.lower()
    
#     # Loại bỏ các ký tự không mong muốn
#     result_str = ''.join(c for c in result_str if c.isalnum() or c.isspace())
    
#     return result_str

# input_string = f'{random.choice(FIRST_NAME)}{random.choice(MID_NAME)}{random.choice(MID_NAME)}{random.randint(100, 10000)}'
# output_string = remove_accents(input_string)
# print(output_string)