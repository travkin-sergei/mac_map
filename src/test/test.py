"""
Тестирование прокси на состоятельность
"""

import uuid
import requests

from urllib3.util import Retry
from requests.adapters import HTTPAdapter

session = requests.Session()

retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))
session_id = uuid.uuid4()

proxy = {
    'http': 'http://116.125.141.115:80',
    # 'https': 'https:45.133.75.125:3128'
    # 'SOCKS5': 'SOCKS5://139.162.78.109:1080'
}
url = 'https://ipinfo.io/json'

data = session.get(url, proxies=proxy)
print(data.text)
