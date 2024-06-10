import requests

prox = {'http': 'http://mGRWQE9F:tFk4qw8D@85.142.82.98:63502'}

# proxies = {'https': 'https://Fv4Z8e:ABMCPU@217.29.53.64:11835'}
url = 'http://ipinfo.io/json'

response = requests.get(url, proxies=prox)
print(response.json())
