import re
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


@logger_fun
def convert_string(text):
    """
    Преобразование строки:
        a) унификация переносов строк
        b) удаление непечатных символов
        c) удаление лишних пробелов
        d) удаление лишних переносов строк
        e) дублирующих кавычек
        f) лишних кавычек
    :param text: str
    :return: str
    """
    # a) унификация переносов строк
    pattern = r'[\r\n\u0085\u2028\u2029\t]'
    text = re.sub(pattern, '\n', text)
    # b) удаление непечатных символов
    pattern = r'[\x00-\x1F\x7F-\x9F\u200B\u200C\u200D\uFEFF]'
    text = re.sub(pattern, "", text)
    # c) удаление лишних пробелов
    text = re.sub(r'\s+', ' ', text)
    # d) удаление лишних переносов строк
    text = re.sub(r'\n+', '\n', text)
    words = text.split(' ')
    result = []
    # e) дублирующих кавычек
    for word in words:
        word = re.sub(r'^""', '«', word)  # Начальные двойные кавычки
        word = re.sub(r'""$', '»', word)  # Конечные двойные кавычки
        word = word.replace('""', '»')  # Остальные двойные кавычки
        result.append(word)
    # f) лишних кавычек
    res = re.sub(r'^"|"$', '', ' '.join(result))  # Удаление одиночных кавычек по краям
    # Удаление непарных кавычек. Простая замена не сделана т.к. надо найти другие ошибки и обработать их
    return res.replace('»"»', '»»')
