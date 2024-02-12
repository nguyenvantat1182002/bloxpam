from victims import *
from tinproxy import TinProxy, ProxyError
from chrome_fingerprints import FingerprintGenerator

import time
import queue
import json
import threading
import capsolver
capsolver.api_key = "CAP-FFE2271E0A6E1961C4FB2BF717C81F0D"


CHROME_WIDTH, CHROME_HEIGHT = 262, 400


def main(init_lock: threading.Lock, close_lock: threading.Lock, tinproxy: TinProxy, account_list: queue.Queue, chrome_pos: tuple, fp_gen: FingerprintGenerator):
    while True:
        try:
            proxy = tinproxy.get_new_proxy()
            if not proxy:   
                end_time = time.time() + tinproxy.next_request
                while True:
                    if time.time() > end_time:
                        break
                    print('Se lay lai proxy sau', int(end_time - time.time()))
                    time.sleep(1)
            
            with init_lock:
                victim = bidaithanroblox(proxy)
                victim.driver.set.window.size(CHROME_WIDTH, CHROME_HEIGHT)
                victim.driver.set.window.location(*chrome_pos)
            # victim = dichvurobux(proxy, fp_gen)
            # victim.run()
            # with init_lock:
            #     if account_list.empty():
            #         return
            #     data: str = account_list.get_nowait()
            #     account_list.task_done()
            # victim.run(*data.split('|'))
            account = victim.run()
            if account is not None:
                with init_lock:
                    with open('bi_acc.txt', 'a', encoding='utf-8') as file:
                        file.write('|'.join(account) + '\n')
            # with init_lock:
            #     if account_list.empty():
            #         return
            #     data: str = account_list.get_nowait()
            #     account_list.task_done()
            #     username, password = data.split('|')
            # victim.run(username, password)
            # username, password = victim.run('username', 'password')
            # with init_lock:
            #     with open('acc.txt', 'a', encoding='utf-8') as file:
            #         file.write(f'{username}|{password}\n')
        except ProxyError as e: 
            print(e) 
            return 
        except Exception as e:
            print(type(e).__name__)
        finally:
            with close_lock:
                try:
                    victim.close()
                except Exception:
                    pass


with open('config.json', encoding='utf-8') as file:
    config = json.load(file)

with open('api.txt', encoding='utf-8') as file:
    tinproxy_keys = file.readlines()
    tinproxy_keys = map(lambda item: item.strip(), tinproxy_keys)

tinproxy_instances = queue.Queue()
for item in tinproxy_keys:
    tinproxy_instances.put(TinProxy(item))

account_list = queue.Queue()
with open('biacc.txt', encoding='utf-8') as file:
    lines = file.read().splitlines()
for item in lines:
    account_list.put_nowait(item)

rows = config['Rows']
columns = config['Columns']

if (columns * rows) > tinproxy_instances.qsize():
    print('TinProxy keys khong du.')
    exit(1)

threads = []
x, y = 0, 0
init_lock = threading.Lock()
close_lock = threading.Lock()
fp_gen = FingerprintGenerator()

for r in range(rows):
    for c in range(columns):
        if tinproxy_instances.qsize() < 1:
            break
        tinproxy = tinproxy_instances.get()
        threads.append(
            threading.Thread(
                    target=main,
                    args=(init_lock, close_lock, tinproxy, account_list, (x, y), fp_gen),
                    daemon=True
                )
            )
        x += int(CHROME_WIDTH * 2)
    x = 0
    y += CHROME_HEIGHT

for item in threads:
    item.start()
for item in threads:
    item.join()
    
