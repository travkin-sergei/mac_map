"""
Перевод ТН ВЭД
"""
import time
import multiprocessing
from deep_translator import GoogleTranslator
from src.prod.site.orm import get_products_name, set_products2


def translated_text(text: str):
    """
    Перевод текста с помощью гугла
    """
    translated = GoogleTranslator(source='auto', target='ru', ).translate(text)
    return translated


def process_country(i_name):
    try:
        name_ru = translated_text(i_name[0])
        print(f' name_ru:{name_ru}')
        set_products2(i_name[0], name_ru)
    except:
        print(f'fatal')
        time.sleep(60)


if __name__ == '__main__':
    with multiprocessing.Pool(processes=6) as pool:
        pool.map(process_country, get_products_name())
