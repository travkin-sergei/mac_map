"""Получить национальные кода стран по списку."""

import json
import time
import pandas as pd
import logging
from io import StringIO

from src.prod.site.class_site import Macmap
from src.prod.site.function import hash_sum_256, convert_string
from src.prod.site.orm import ormCreateTable, get_county
from src.prod.system.database import engine_sync

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Инициализация
ormCreateTable()
mac_map = Macmap()
error_list = []

# Получение списка стран плохой способ. Используй список реальных стран
county_list = ['260', '262']

for i_country in county_list:
    try:
        version = mac_map.latest_hs_rev(i_country)
        # Проверяем есть ли данные
        if version:
            tn_ved_list = mac_map.products(i_country)

            # Используем StringIO для чтения JSON
            json_data = json.dumps(tn_ved_list)
            df = pd.read_json(StringIO(json_data), dtype={"Code": str, "Name": str})

            # добавление версии Гармонизированной системы
            df['classification_code'] = version.get('RevCode')
            df['classification_description'] = version.get('RevDesc')
            # Переименовать столбцы
            df = df.rename(columns={
                'Code': 'code',
                'Name': 'name',
                'RevCode': 'name',
                'RevDesc': 'name',
            })
            # Очистка данных от лишних символов
            df['name'] = df['name'].apply(convert_string)
            df['country'] = i_country
            df['hash_address'] = df.apply(lambda x: hash_sum_256(x['country'], x['code']), axis=1)

            # Запись в базу данных
            df.to_sql('temp_products', engine_sync, schema='macmap', if_exists='append', index=False)
            time.sleep(90)
    except Exception as error:
        logging.error(f'Ошибка: Страна = {i_country}, Ошибка = {error}')
        error_list.append(i_country)
        time.sleep(90)

logging.info(f'Не смог проверить: {error_list}')
