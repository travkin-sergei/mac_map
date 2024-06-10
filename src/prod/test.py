import json
import time
from threading import Thread
from src.prod.site.class_site import MacMap, MacMapResults
from src.prod.site.log import logger_fun
from src.prod.site.orm import (
    ormCreateTable,
    customDutiesUpdate,
    customDutiesLevelUpdate,
    getProducts,
    setProducts, ntmMeasuresUpdate, measuresUpdate, allMeasuresUpdate, getPlan, setPlan,
)


@logger_fun
def threading_list(year, results, i_code):
    """Запись тарифов"""
    info = results.customDutiesByYear(year)
    if info.get('NTLCCodeLabel'):
        customDutiesUpdate(i_code.id, info)
        customDutiesLevelUpdate(i_code.id, info)


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
    '008', '032', '050', '064', '070', '072', '096', '108', '144', '158', '204', '222', '242', '270', '288', '308',
    '324', '344', '352', '360', '376', '384', '404', '426', '430', '446', '458', '466', '480', '516', '520', '524',
    '562', '566', '586', '608', '624', '646', '686', '690', '694', '699', '702', '710', '748', '768', '776', '788',
    '800', '834', '854', '862', '876',
]


def main():
    ormCreateTable()
    # updating directories
    mac_map = MacMap()
    countries = mac_map.countries()
    country_list = [i['Code'] for i in countries]
    # ---------------------------------------------- update Products STOP ----------------------------------------------
    for i_country in country_list:
        if i_country in '032':
            # country_code = getProducts(i_country)
            country_code = getPlan(i_country)
            # count = 0
            for i_code in country_code:
                # mac_map_results1 = MacMapResults(i_country, '643', i_code.code)
                mac_map_results1 = MacMapResults(i_country, '643', i_code.tn_ved)
                list_year = [int(i['Year']) for i in mac_map.getYears(i_country)]
                threads = []
                for year in list_year:
                    threading_list(year, mac_map_results1, i_code)
                    t = Thread(target=threading_list, args=(year, mac_map_results1, i_code,))
                    t.start()
                    threads.append(t)
                for t in threads:
                    t.join()
                # mac_map_results2 = MacMapResults(i_country, '643', i_code.code)
                mac_map_results2 = MacMapResults(i_country, '643', i_code.tn_ved)
                measures_list(mac_map_results2, i_code)
                setPlan(i_code.id)

                # count += 1


# Все что ниже удалить если включать в Airflow
if __name__ == '__main__':
    exit(main())
else:
    raise SystemExit("Это не библиотека")
