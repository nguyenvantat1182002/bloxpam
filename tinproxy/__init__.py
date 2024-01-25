import requests


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'


class ProxyError(Exception):
    pass


class TinProxy:
    _api_key: str
    _request: requests.Session
    _next_request: int

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._request = requests.Session()
        self._next_request = 0

        self.request.headers.update({
            'User-Agent': USER_AGENT
        })

    @property
    def next_request(self) -> int:
        return self._next_request
    
    @next_request.setter
    def next_request(self, value: int):
        self._next_request = value

    @property
    def request(self) -> requests.Session:
        return self._request
    
    def get_new_proxy(self) -> str:
        response = self.request.get(
            url='https://api.tinproxy.com/proxy/get-new-proxy',
            params={'api_key': self._api_key}
        )
        data = response.json()

        try:
            data = data['data']
            http_ipv4 = data['http_ipv4']
            authentication = data['authentication']
            username = authentication['username']
            password = authentication['password']
            self.next_request = data['next_request']
        except Exception:
            raise ProxyError(data)
        
        if len(http_ipv4) < 6 or len(username) < 3 or len(password) < 3:
            return None

        return f'{username}:{password}@{http_ipv4}'
    