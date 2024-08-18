"""
Получение списка Национальных кодов ТН ВЭД
подробнее на сайте - https://www.macmap.org/en/resources/product-search?reporter=004&keyword=010110&level=false
"""
import json
import time
import pandas as pd
from src.prod.site.class_site import Macmap
from src.prod.site.function import hash_sum_256
from src.prod.site.orm import ormCreateTable, get_county
from src.prod.system.database import engine_sync

replace_dict = {
    '""""""': '"',
    '"""""': '"',
    '""""': '"',
    '"""': '"',
    '""': '"',
    '¬¬--': '',
    '\n': ' ',
    '\t': ' ',
    '&nbsp;': ' ',
}
address = r'C:\Users\Sergei\Downloads\MacMap'
ormCreateTable()
mac_map = Macmap()
error_list = []
for i_country in get_county():
    try:
        tn_ved_list = mac_map.products(i_country)
        # hash_sum_256()
        df = pd.read_json(json.dumps(tn_ved_list),dtype={"Code": str, "Name": str})
        df.to_csv(f'{address}/json/{i_country}.json')
        # переименовать столбцы
        df = df.rename(columns={'Code': 'code', 'Name': 'name'})
        # очистка данных от лишних символов
        df['name'] = df['name'].replace(replace_dict, regex=True)
        df['country'] = i_country
        df['hash_address'] = df.apply(lambda x: hash_sum_256(x['country'], x['code']), axis=1)
        # запись в базу данных
        df.to_csv(f'{address}/csv/{i_country}.csv')
        df.to_sql('products2', engine_sync, schema='macmap', if_exists='append', index=False)
    except:
        print(f'Ошибка: Страна = {i_country}')
        error_list.append(i_country)
        time.sleep(22)
print(f'Не смог проверить: {error_list}')
