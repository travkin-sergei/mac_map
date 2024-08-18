"""
Получение целевых данных с сайта macmap
"""


import concurrent.futures

from src.prod.site.orm import (
    ormCreateTable,
    customDutiesUpdate,
    customDutiesLevelUpdate,
    get_plan, set_plan,
    ntmMeasuresUpdate, measuresUpdate, allMeasuresUpdate, get_county
)
from src.prod.site.class_site import Macmap



priorities_list = [
    '288', '324', '344', '384', '404', '426', '428', '430',
    '440', '442', '446', '466', '480', '490', '516', '520',
]


def process_country(i_country):
    country_code = get_plan(i_country)
    mac_map1 = Macmap()
    max_year = [max([int(i['Year']) for i in mac_map1.getYears(i_country)])]
    for i_code in country_code:
        mac_map2 = Macmap()

        info = mac_map2.custom_duties_by_year(i_country, i_code.tn_ved, max_year, )
        if info.get('NTLCCodeLabel'):
            customDutiesUpdate(i_code.id, info)
            customDutiesLevelUpdate(i_code.id, info)

        for i_e in ['M', 'X']:
            data = mac_map2.ntm_measure_by_regulation(i_country, i_code.tn_ved, i_e).json()
            if data:
                ntmMeasuresUpdate(i_code.id, data)
                measuresUpdate(i_e, i_code.id, data)
                allMeasuresUpdate(i_e, i_code.id, data)
        set_plan(i_code.id)
        print(f'Страна: {i_country} год: {max_year}')


def main():
    ormCreateTable()
    country_list = get_county()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_country, i_country) for i_country in country_list if i_country in priorities_list]
        for future in concurrent.futures.as_completed(futures):
            future.result()


if __name__ == '__main__':
    exit(main())
else:
    raise SystemExit("Это не библиотека")