import re
import sys
import hashlib
import requests

from src.prod.site.log import logConect

log = logConect()
MAX_RETRIES = 3


def hashSum256(*args):
    try:
        list_str = [str(i) for i in args]
        list_union = '+'.join(list_str)
        ha256 = hashlib.sha256(list_union.encode()).hexdigest()
        return ha256
    except Exception as error:
        log.error(f'def {sys._getframe().f_code.co_name}: {error}')


def requestsGet(link, params, **kwargs):
    try:
        requestsGet.call_count += 1
        count_get = requestsGet.call_count
    except AttributeError:
        requestsGet.call_count = 1
        count_get = requestsGet.call_count

    proxies = {
        'https': 'socks5://mGRWQE9F:tFk4qw8D@85.142.130.211:62679'
    }
    result = None
    for _ in range(MAX_RETRIES):
        try:
            result = requests.get(link, params, **kwargs, )
            match result.status_code == 200:
                case 200:
                    result.encoding = 'utf-8'
                    result.raise_for_status()
                    log.info(f'def {sys._getframe().f_code.co_name}: {result.status_code}')
                    break
                case 403:
                    log.info(f'def {sys._getframe().f_code.co_name}: {result.status_code}')
                    exit()
                case 404:
                    log.info(f'def {sys._getframe().f_code.co_name}: {result.status_code}')
                    exit()
                case 500:
                    log.info(f'def {sys._getframe().f_code.co_name}: {result.status_code}')
                    exit()
                case _:
                    pass
        except Exception as error:
            log.exception(f'def {sys._getframe().f_code.co_name}: {error}')
    else:
        log.error(f'def {sys._getframe().f_code.co_name}. All retries failed')
    return result


def camelToSnake(data):
    for old_key in data:
        for old_key in data:
            for old_key in data:
                new_key = re.sub(r'(?<!^)(?=[A-Z])', '_', old_key).lower()
        print(old_key, ';', new_key)
    return data
