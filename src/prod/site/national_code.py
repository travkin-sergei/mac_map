import json
import os
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

# Создание необходимых директорий
address = r'C:\Users\travk\Downloads\MacMap'
json_dir = os.path.join(address, 'json')
if not os.path.exists(json_dir):
    os.makedirs(json_dir)

csv_dir = os.path.join(address, 'csv')
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

# Инициализация
ormCreateTable()
mac_map = Macmap()
error_list = []

# Получение списка стран
county_list = [i.get('Code') for i in mac_map.countries()]

for i_country in county_list:
    try:
        tn_ved_list = mac_map.products(i_country)

        # Используем StringIO для чтения JSON
        json_data = json.dumps(tn_ved_list)
        df = pd.read_json(StringIO(json_data), dtype={"Code": str, "Name": str})

        # Сохранение в JSON
        df.to_json(f'{json_dir}/{i_country}.json', orient='records', lines=True)

        # Переименовать столбцы
        df = df.rename(columns={'Code': 'code', 'Name': 'name'})

        # Очистка данных от лишних символов
        df['name'] = df['name'].apply(convert_string)
        df['country'] = i_country
        df['hash_address'] = df.apply(lambda x: hash_sum_256(x['country'], x['code']), axis=1)

        # Запись в CSV
        df.to_csv(f'{csv_dir}/{i_country}.csv', index=False)

        # Запись в базу данных
        df.to_sql('products2', engine_sync, schema='macmap', if_exists='append', index=False)

    except Exception as e:
        logging.error(f'Ошибка: Страна = {i_country}, Ошибка = {e}')
        error_list.append(i_country)
        time.sleep(90)

logging.info(f'Не смог проверить: {error_list}')