import sys

from src.prod.site.function import requestsGet
from src.prod.site.log import logConect
from src.prod.system.database import engine_sync
from src.prod.system.models import Base

log = logConect()


# ==================================================== Create Class ====================================================
def getApi(link_api, params, headers):
    """for the MacMapResults model"""
    try:
        result = requestsGet(link_api, params=params, headers=headers)
        if result.status_code == 200:
            return result.json()
        else:
            log.warning(f'def {sys._getframe().f_code.co_name}: {result.status_code}')
    except Exception as error:
        log.error(f'def {sys._getframe().f_code.co_name}: {error}')


class MacMap():
    host = "www.macmap.org"
    url_base = 'https://{0}'.format(host)
    api_base = 'https://www.macmap.org/api'
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01"
        , "User-Agent": "Safari/537.3"
        , "User": "@sergei9_94. I'll download it anyway, but I don't want to cause you any problems."
        , "Host": host
    }

    def __init__(self, host=host, url_base=url_base, api_base=api_base, headers=headers):
        self.host = host
        self.url_base = url_base
        self.headers = headers
        self.api_base = api_base

    # получаем список стран
    def countries(self):
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        link_api = '{0}/countries'.format(self.api_base)
        result = requestsGet(link_api, params=None, headers=self.headers)
        if result is None:
            log.warning(f'def {sys._getframe().f_code.co_name}: result is None ')
        else:
            if result.status_code == 200:
                return result.json()
            else:
                log.warning(f'def {sys._getframe().f_code.co_name}: {result.status_code}')

    def products(self, country_code):
        """ national HS code """
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        params = {
            "countryCode": country_code
            , "level": 8
        }
        link_api = '{0}/products'.format(self.api_base)
        result = requestsGet(link_api, params=params, headers=self.headers)

        if result.status_code == 200:
            return result.json()
        else:
            log.warning(f'def {sys._getframe().f_code.co_name}: {result.status_code}')

    def products_by_keyword(self, exporting_code, tn_ved_2: str):
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        params = {
            "countryCode": exporting_code
            , "level": 6
            , "keyword": tn_ved_2
        }
        link_api = '{0}/v2/products-by-keyword'.format(self.api_base)
        result = requestsGet(link_api, params=params, headers=self.headers)

        if result.status_code == 200:
            return result.json()
        else:
            log.warning(f'def {sys._getframe().f_code.co_name}: {result.status_code}')

    def ntlc_product(self, exporting_code: str, tn_ved_code: str):
        self.headers["Referer"] = 'https://{0}'.format(self.host)
        params = {
            "countryCode": exporting_code
            , "level": 8
            , "code": tn_ved_code
        }
        link_api = '{0}/v2/ntlc-products'.format(self.api_base)
        result = requestsGet(link_api, params=params, headers=self.headers)

        if result.status_code == 200:
            return result.json()
        else:
            log.warning(f'def {sys._getframe().f_code.co_name}: {result.status_code}')


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
        ] = '{url_base}/{language}//query/results?reporter={rep}&partner={par}&product={tn_ved}&level=6'.format(
            url_base=url_base, language=language, rep=reporter, par=partner, tn_ved=tn_ved_10
        )
        self.params = {
            "reporter": reporter
            , "partner": partner
            , "product": tn_ved_10
        }

    def customduties(self):
        link_api = '{0}/customduties'.format(self.api_base)
        result = getApi(link_api, params=self.params, headers=self.headers)
        return result

    def tariff_regime_country_list(self):
        data = self.customduties()
        result_data = []
        for i_data in data.get("CustomDuty"):
            params = {
                "agId": i_data.get("AgreementID"),
                "reporter": self.reporter,
                "year": "latest",
            }
            link_api = '{0}/tariff-regime-country-list'.format(self.api_base)
            result = getApi(link_api, params=params, headers=self.headers)
            result_data.append(result)
        return result_data

    def ntm_measures(self):
        link_api = '{0}/ntm-measures'.format(self.api_base)
        result = getApi(link_api, params=self.params, headers=self.headers)
        return result

    def traderemedy(self):
        link_api = '{0}/traderemedy'.format(self.api_base)
        result = getApi(link_api, params=self.params, headers=self.headers)
        return result

    def taxes(self):
        link_api = '{0}/taxes'.format(self.api_base)
        result = getApi(link_api, params=self.params, headers=self.headers)
        return result
