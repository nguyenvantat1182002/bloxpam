# from victims import *
# from chrome_fingerprints import FingerprintGenerator


# fp_gen = FingerprintGenerator()
# victim = hiddingroblox(None, fp_gen)
# victim.check2('hiddingroblox.txt', victim.get_items)
# victim.run()

# import capsolver
# capsolver.api_key = "CAP-FFE2271E0A6E1961C4FB2BF717C81F0D"


# victim = shoptridung('brZgipEN:OvBNcLMk@171.235.160.120:21001', fp_gen)
# victim.run()

from DrissionPage import ChromiumPage, ChromiumOptions


import time


options = ChromiumOptions().auto_port(tmp_path='profiles')
options.set_proxy('http://127.0.0.1:4000')
driver = ChromiumPage(addr_or_opts=options)
try:
    driver.get('https://www.facebook.com/', show_errmsg=True, retry=1)
    time.sleep(4)
except Exception:
    pass
driver.quit()



