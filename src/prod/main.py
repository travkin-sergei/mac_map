"""
Получение целевых данных с сайта macmap
"""

import concurrent.futures
import time

from src.prod.site.orm import (
    ormCreateTable,
    customDutiesUpdate,
    customDutiesLevelUpdate,
    get_plan, set_plan,
    ntmMeasuresUpdate,
    measuresUpdate,
    allMeasuresUpdate,
    get_county
)
from src.prod.site.class_site import Macmap

priorities_list = [
    # '008', '040', '050', '056', '070', '072', #2024-08-29
    # '100', '108', '156', '204', '222', '233',
    # '242', '246', '251', '270', '288', '324',
    '344', '384', '404', '426', '428', '430',
    # '440', '442', '446', '466', '480', '490',
    # '516', '520', '524', '528', '562', '566',
    # '585', '586', '598', '616', '624', '642',
    # '646', '686', '694', '699', '702', '703',
    # '710', '724', '748', '768', '788', '792',
    # '800', '834', '854', '876', '895', '894',
    #
    # '036', '048', '064', '191', '196', '203',
    # '208', '258', '276', '300', '332', '348',
    # '360', '372', '380', '388', '414', '458',
    # '462', '470', '499', '504', '508', '512',
    # '531', '554', '583', '608', '620', '634',
    # '682', '688', '705', '706', '752', '784',

]


def process_country(i_country):
    try:
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
    except Exception as error:
        print(f'==============fatal: \n{error}')
        time.sleep(60)


def main():
    ormCreateTable()
    country_list = get_county()

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(process_country, i_country) for i_country in country_list if
                   i_country in priorities_list]
        for future in concurrent.futures.as_completed(futures):
            future.result()


if __name__ == '__main__':
    exit(main())
else:
    raise SystemExit("Это не библиотека")
