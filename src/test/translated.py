"""
Перевод ТН ВЭД
"""
import time
import multiprocessing
from deep_translator import GoogleTranslator
from src.prod.site.orm import get_products2, set_products2, get_county


def translated_text(text: str):
    """
    Перевод текста с помощью гугла
    """
    translated = GoogleTranslator(source='auto', target='ru', ).translate(text)
    return translated


def process_country(i_country):
    try:
        for i in get_products2():
            name_ru = translated_text(i.name)
            print(f'country:{i_country}, name_ru:{name_ru},id:{i.id}')
            set_products2(i.id, name_ru)
    except:
        print(f'{i_country}')
        time.sleep(10)


if __name__ == '__main__':
    with multiprocessing.Pool(processes=10) as pool:
        pool.map(process_country, get_county())
