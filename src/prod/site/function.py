import re
import sys
import hashlib
import time



from src.prod.site.log import logger_fun

MAX_RETRIES = 3


@logger_fun
def hash_sum_256(*args):
    """
    Получить хеш суму из args
    """
    list_str = [str(i) for i in args]
    list_union = '+'.join(list_str)
    ha256 = hashlib.sha256(list_union.encode()).hexdigest()
    return ha256


@logger_fun
def requests_get(session, link, params, **kwargs):
    try:
        requests_get.call_count += 1
        count_get = requests_get.call_count
    except AttributeError:
        requests_get.call_count = 1
        count_get = requests_get.call_count

    proxy = {'http': 'http://xHdTAr:SpE6Rc@95.164.128.227:9842'}
    result = None
    for _ in range(MAX_RETRIES):

        # result = requests.get(link, params, **kwargs, )
        result = session.get(link, params=params, **kwargs)  # ,  proxies=proxy)

        print(result.status_code)
        match result.status_code:
            case 200:
                result.encoding = 'utf-8'
                result.raise_for_status()
                break
            case 403:

                exit()
            case 404:

                exit()
            case 500:

                exit()
            case _:
                time.sleep(40)

    return result


@logger_fun
def camel_to_snake(data):
    """
    Изменить сталь написания с CamelCase на snake_case
    """
    for old_key in data:
        for old_key in data:
            for old_key in data:
                new_key = re.sub(r'(?<!^)(?=[A-Z])', '_', old_key).lower()
        print(old_key, ';', new_key)
    return data
