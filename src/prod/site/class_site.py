import uuid
import requests
from fake_useragent import UserAgent

from urllib3.util import Retry
from requests.adapters import HTTPAdapter

from src.prod.site.function import requests_get


class Macmap:
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session_id = uuid.uuid4()
    host = "www.macmap.org"
    url_base = 'https://{0}'.format(host)
    api_base = 'https://www.macmap.org/api'

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01'
        , 'Accept-Encoding': 'gzip, deflate, br, zstd'
        , 'Accept-Language': 'en-US,en;q=0.9'
        , 'Cache-Control': 'no-cache'
        , 'Connection': 'keep-alive'
        , 'Content-Type': 'application/json; charset=utf-8'
        , 'Cookie': f'ASP.NET_SessionId={session_id}; path=/; secure; HttpOnly; SameSite=None; SameSite=None; Secure'
        , 'Dnt': '1'
        , 'Host': host
        , 'Pragma': 'no-cache'
        , 'Sec-Ch-Ua': '"Not(A:Brand";v="24", "Chromium";v="122"'
        , 'X-Requested-With': 'XMLHttpRequest'
        , 'X-Kl-Ajax-Request': 'Ajax_Request'
        , 'Sec-Ch-Ua-Mobile': '?0'
        , 'User-Agent': UserAgent().random
        , 'Sec-Ch-Ua-Platform': '"Windows"'
        , 'Sec-Fetch-Site': 'same-origin'
        , 'Sec-Fetch-Mode': 'cors'
        , 'Sec-Fetch-Dest': 'empty'
        , 'Priority': 'u=1, i'

    }

    # получаем список стран
    def countries(self):
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        link_api = '{0}/countries'.format(self.api_base)
        result = requests_get(self.session, link_api, params=None, headers=self.headers)  # proxies=proxy)
        if result:
            if result.status_code == 200:
                return result.json()

    def customDuties(self, reporter, partner, tn_ved_10):
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        params = {
            "reporter": reporter
            , "partner": partner
            , "product": tn_ved_10
        }
        link_api = '{0}/results/customduties'.format(self.api_base)
        result = requests_get(self.session, link_api, params=params, headers=self.headers)  # proxies=proxy)
        return result

    def getYears(self, reporter_code) -> str:
        """
        for
        def custom_duties_by_year():
            pass
        https://www.macmap.org/api/getyears?datatype=Tariff&reporters=466
        """
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        params = {
            "datatype": "Tariff",
            "reporters": reporter_code,
        }
        link_api = '{0}/getyears'.format(self.api_base)
        result = requests_get(self.session, link_api, params=params, headers=self.headers)  # proxies=proxy)

        if result.status_code == 200:
            return result.json()

    def custom_duties_by_year(self, reporter, tn_ved, year):
        """
        def getYears():
            https://www.macmap.org/api/getyears?datatype=Tariff&reporters=466
            ...
        1) https://www.macmap.org/ru/query/customs-duties?reporter=466&year=2024&partner=all&product=220190&level=6
        2) data = getYears()
        3) https://www.macmap.org/api/results/custom-duties-by-year?reporter=466&partner=all&product=2201900000&year=2024
        """
        params = {
            "reporter": reporter,
            "partner": "all",
            "product": tn_ved,
            "year": year,
        }
        link_api = '{0}/results/custom-duties-by-year'.format(self.api_base)
        result = requests_get(self.session, link_api, params=params, headers=self.headers)  # proxies=proxy)
        if result.status_code == 200:
            return result.json()

    def ntm_measure_by_regulation(self, reporter, tn_ved_10, direction):
        """
        direction
        I - Import
        E - Export
        """
        params = {
            "reporter": reporter
            , "partner": '643'
            , "product": tn_ved_10
        }
        link_api = '{0}/results/ntm-measure-by-regulation'.format(self.api_base)
        params['regType'] = direction
        result = requests_get(self.session, link_api, params=params, headers=self.headers)  # proxies=proxy)
        return result

    def products_by_keyword(self, exporting_code, tn_ved_2: str):
        """Получение кода ТН ВЭД 6 знаков по первым 2м символам"""
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        params = {
            "countryCode": exporting_code
            , "level": 6
            , "keyword": tn_ved_2
        }
        link_api = '{0}/v2/products-by-keyword'.format(self.api_base)
        result = requests_get(self.session, link_api, params=params, headers=self.headers)  # proxies=proxy)
        if result.status_code == 200:
            return result.json()

    def ntlcProduct(self, exporting_code: str, tn_ved_code: str):
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        params = {
            "countryCode": exporting_code
            , "level": 8
            , "code": tn_ved_code
        }
        link_api = '{0}/v2/ntlc-products'.format(self.api_base)

        result = requests_get(self.session, link_api, params=params, headers=self.headers)  # proxies=proxy)
        if result.status_code == 200:
            return result.json()

    def products(self, code):
        """
        Получение списка ТН ВЭД для каждой страны отдельно
        link = https://www.macmap.org/api/products?countryCode=004&level=8
        """
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        params = {
            "countryCode": code,
            "level": 8,
        }
        link_api = '{0}/products'.format(self.api_base)
        result = requests_get(self.session, link_api, params=params, headers=self.headers)  # proxies=proxy)
        if result.status_code == 200:
            return result.json()
