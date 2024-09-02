import requests

proxy_login = '4bixbVig'
proxy_password = '7FB7p7y2'
proxy_port = '85.143.48.112:63478'

proxy = {
    'http': f'http://{proxy_login}:{proxy_password}@{proxy_port}',
    'https': f'https://{proxy_login}:{proxy_password}@{proxy_port}',  # Update this line
}

url = 'https://ipinfo.io/json'

try:
    response = requests.get(url, proxies=proxy)
    print(response.json())
except requests.exceptions.RequestException as e:
    print("Proxy is not working:", e)
