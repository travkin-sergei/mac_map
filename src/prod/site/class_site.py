import uuid
import requests
from fake_useragent import UserAgent

from urllib3.util import Retry
from requests.adapters import HTTPAdapter

from src.prod.site.function import requests_get


# ==================================================== Create Class ====================================================

class MacMap():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session_id = uuid.uuid4()
    host = "www.macmap.org"
    url_base = 'https://{0}'.format(host)
    api_base = 'https://www.macmap.org/api'

    headers = {
        'Cookie': f'ASP.NET_SessionId={session_id}; path=/; secure; HttpOnly; SameSite=None; SameSite=None; Secure'
        , 'Sec-Ch-Ua': '"Not(A:Brand";v="24", "Chromium";v="122"'
        , 'Accept': 'application/json, text/javascript, */*; q=0.01'
        , 'Content-Type': 'application/json; charset=utf-8'
        , 'X-Requested-With': 'XMLHttpRequest'
        , 'Sec-Ch-Ua-Mobile': '?0'
        , 'User-Agent': UserAgent().random
        , 'Sec-Ch-Ua-Platform': '"Windows"'
        , 'Sec-Fetch-Site': 'same-origin'
        , 'Sec-Fetch-Mode': 'cors'
        , 'Sec-Fetch-Dest': 'empty'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Accept-Language': 'en-US,en;q=0.9'
        , 'Priority': 'u=1, i'
        , 'Connection': 'close'
    }

    # получаем список стран
    def countries(self):
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        link_api = '{0}/countries'.format(self.api_base)
        result = requests_get(self.session, link_api, params=None, headers=self.headers, )  # proxies=proxy)
        if result:
            if result.status_code == 200:
                return result.json()

    def products(self, country_code):
        """ national HS code """
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        params = {
            "countryCode": country_code
            , "level": 8
        }
        link_api = '{0}/products'.format(self.api_base)
        result = requests_get(self.session, link_api, params=params, headers=self.headers, )  # proxies=proxy)
        if result.status_code == 200:
            return result.json()

    def productsByKeyword(self, exporting_code, tn_ved_2: str):
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        params = {
            "countryCode": exporting_code
            , "level": 6
            , "keyword": tn_ved_2
        }
        link_api = '{0}/v2/products-by-keyword'.format(self.api_base)
        result = requests_get(self.session, link_api, params=params, headers=self.headers, )  # proxies=proxy)

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

        result = requests_get(self.session, link_api, params=params, headers=self.headers, )  # proxies=proxy)
        if result.status_code == 200:
            return result.json()

    def getYears(self, exporting_code) -> str:
        """
        for
        def custom_duties_by_year():
            pass
        https://www.macmap.org/api/getyears?datatype=Tariff&reporters=466
        """
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        params = {
            "datatype": "Tariff",
            "reporters": exporting_code,
        }
        link_api = '{0}/getyears'.format(self.api_base)
        result = requests_get(self.session, link_api, params=params, headers=self.headers, )  # proxies=proxy)

        if result.status_code == 200:
            return result.json()

    def getFtaListByCountry(self, exporting_code, is_exporter: bool):
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        params = {
            "countrycode": exporting_code,
            "isimporter": "True" if is_exporter else "False",
            "isexporter": "False" if is_exporter else "True",
            "partnercode": "ALL",
        }
        link_api = '{0}/getftalistbycountry'.format(self.api_base)
        result = requests_get(self.session, link_api, params=params, headers=self.headers, )  # proxies=proxy)

        if result.status_code == 200:
            return result.json()


class MacMapResults(MacMap):
    """exporting_code = reporter"""
    url_base = MacMap.url_base
    headers = MacMap.headers
    api_base = MacMap.api_base

    def __init__(
            self, reporter, partner, tn_ved_10, language='en'
            , url_base=url_base
            , headers=headers
            , api_base=api_base
    ):
        self.reporter = reporter
        self.partner = partner
        self.tn_ved = tn_ved_10
        self.language = language
        self.api_base = '{0}/results'.format(api_base)
        self.headers = headers
        headers[
            "Referer"
        ] = '{url_base}/{language}//query/results?reporter={rep}&partner={par}&product={tn_ved}&level=8'.format(
            url_base=url_base, language=language, rep=reporter, par=partner, tn_ved=tn_ved_10
        )
        self.params = {
            "reporter": reporter
            , "partner": partner
            , "product": tn_ved_10
        }

    def customDuties(self):
        link_api = '{0}/customduties'.format(self.api_base)
        result = requests_get(self.session, link_api, params=self.params, headers=self.headers, )  # proxies=proxy)
        return result

    def customDutiesByYear(self, year):
        """
        def getYears():
            https://www.macmap.org/api/getyears?datatype=Tariff&reporters=466
            ...
        1) https://www.macmap.org/ru/query/customs-duties?reporter=466&year=2024&partner=all&product=220190&level=6
        2) data = getYears()
        3) https://www.macmap.org/api/results/custom-duties-by-year?reporter=466&partner=all&product=2201900000&year=2024
        """
        params = {
            "reporter": self.reporter,
            "partner": "all",
            "product": self.tn_ved,
            "year": year,
        }
        link_api = '{0}/custom-duties-by-year'.format(self.api_base)
        result = requests_get(self.session, link_api, params=params, headers=self.headers, )  # proxies=proxy)
        if result.status_code == 200:
            return result.json()

    def tariffRegimeCountryList(self):
        data = self.customDuties()
        result_data = []
        for i_data in data.get("CustomDuty"):
            params = {
                "agId": i_data.get("AgreementID"),
                "reporter": self.reporter,
                "year": "latest",
            }
            link_api = '{0}/tariff-regime-country-list'.format(self.api_base)
            # result = getApi(link_api, params=params, headers=self.headers)
            result = requests_get(self.session, link_api, params=params, headers=self.headers, )  # proxies=proxy)
            result_data.append(result)
        return result_data

    def ntmMeasures(self):
        link_api = '{0}/ntm-measures'.format(self.api_base)
        # result = getApi(link_api, params=self.params, headers=self.headers)
        result = requests_get(self.session, link_api, params=self.params, headers=self.headers, )  # proxies=proxy)
        return result

    def ntm_measure_by_regulation(self, direction):
        """
        direction
        I - Import
        E - Export
        """
        link_api = '{0}/ntm-measure-by-regulation'.format(self.api_base)
        self.params['regType'] = direction
        result = requests_get(self.session, link_api, params=self.params, headers=self.headers, )  # proxies=proxy)
        return result

    def tradereMedy(self):
        link_api = '{0}/traderemedy'.format(self.api_base)
        # result = getApi(link_api, params=self.params, headers=self.headers)
        result = requests_get(self.session, link_api, params=self.params, headers=self.headers, )  # proxies=proxy)
        return result

    def taxes(self):
        link_api = '{0}/taxes'.format(self.api_base)
        # result = getApi(link_api, params=self.params, headers=self.headers)
        result = requests_get(self.session, link_api, params=self.params, headers=self.headers, )  # proxies=proxy)
        return result
