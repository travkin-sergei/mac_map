"""
Получение целевых данных с сайта macmap
"""

import time

from src.prod.site.log import logger_fun
from src.prod.site.orm import (
    ormCreateTable,
    customDutiesUpdate,
    customDutiesLevelUpdate,
    get_plan, set_plan,
    ntmMeasuresUpdate, measuresUpdate, allMeasuresUpdate
)
from src.prod.site.class_site import Macmap


@logger_fun
def measures_list(results, i_code):
    """Запись мер"""
    for i_e in ['M', 'X']:
        print(f'i_e={i_e}')
        data = results.ntm_measure_by_regulation(i_e).json()
        if data:
            ntmMeasuresUpdate(i_code.id, data)
            measuresUpdate(i_e, i_code.id, data)
            allMeasuresUpdate(i_e, i_code.id, data)


priorities_list = [
    '008', '040', '050', '056', '070', '072', '100', '108', '156', '204', '222', '233', '242', '246', '251', '270',
    '288', '324', '344', '384', '404', '426', '428', '430', '440', '442', '446', '466', '480', '490', '516', '520',
    '524', '528', '562', '566', '585', '586', '598', '616', '624', '642', '646', '686', '694', '699', '702', '703',
    '710', '724', '748', '768', '788', '792', '800', '834', '854', '876', '895',
]


def main():
    ormCreateTable()
    # updating directories
    mac_map1 = Macmap()
    try:
        country_list = [i['Code'] for i in mac_map1.countries()]
        # ---------------------------------------------- update Products STOP ----------------------------------------------
        for i_country in country_list:

            if i_country in priorities_list:
                print(i_country)
                country_code = get_plan(i_country)

                max_year = [max([int(i['Year']) for i in mac_map1.getYears(i_country)])]
                for i_code in country_code:
                    mac_map2 = Macmap()

                    info = mac_map2.custom_duties_by_year(i_country, i_code.tn_ved, max_year, )
                    if info.get('NTLCCodeLabel'):
                        customDutiesUpdate(i_code.id, info)
                        customDutiesLevelUpdate(i_code.id, info)

                    # mac_map_results2 = MacMapResults(i_country, '643', i_code.code)

                    for i_e in ['M', 'X']:
                        data = mac_map2.ntm_measure_by_regulation(i_country, i_code.tn_ved, i_e).json()
                        if data:
                            ntmMeasuresUpdate(i_code.id, data)
                            measuresUpdate(i_e, i_code.id, data)
                            allMeasuresUpdate(i_e, i_code.id, data)
                    set_plan(i_code.id)
                    print(f'Страна: {i_country} год: {max_year}')
    except:
        print('Что-то не так')
        time.sleep(90)


# Все что ниже удалить если включать в Airflow
if __name__ == '__main__':
    exit(main())
else:
    raise SystemExit("Это не библиотека")
