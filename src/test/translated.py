"""
Перевод ТН ВЭД
"""
import time
from deep_translator import GoogleTranslator

from src.prod.site.orm import get_products2, set_products2

import multiprocessing

from src.prod.site.orm import get_products2


def translated_text(text: str):
    """
    Перевод текста
    """
    translated = GoogleTranslator(source='auto', target='ru', ).translate(text)
    return translated


priorities_list = [
    '004', '008', '040', '050', '056', '070', '072', '100', '108',
    '156', '204', '222', '233', '242', '246', '251', '270',
    '288', '324', '344', '384', '404', '426', '428', '430',
    '440', '442', '446', '466', '480', '490', '516', '520',
    '524', '528', '562', '566', '585', '586', '598', '616',
    '624', '642', '646', '686', '694', '699', '702', '703',
    '854', '710', '724', '748', '768', '788', '792', '800',
    '834', '895', '876',
]


def process_country(i_country):
    try:
        for i in get_products2(i_country):
            name_ru = translated_text(i.name)
            print(f'country:{i_country}, name_ru:{name_ru},id:{i.id}')
            set_products2(i.id, name_ru)
    except:
        print(f'{i_country}')
        time.sleep(10)


if __name__ == '__main__':
    with multiprocessing.Pool(processes=10) as pool:
        pool.map(process_country, priorities_list)
