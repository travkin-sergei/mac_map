import time

from src.prod.site.class_site import MacMap, MacMapResults
from src.prod.site.log import logger_fun
from src.prod.site.orm import (
    customDutiesUpdate,
    customDutiesLevelUpdate,
    ntmMeasuresUpdate,
    measuresUpdate,
    allMeasuresUpdate,
    tradeRemedyUpdate,
    taxesUpdate,
    checkingQueryPlan, ormCreateTable,
)

tn_ved_2 = [
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
    '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
    '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
    '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
    '61', '62', '63', '64', '65', '66', '67', '68', '69', '70',
    '71', '72', '73', '74', '75', '76', '77', '78', '79', '80',
    '81', '82' '83', '84', '85', '86', '87', '88', '89', '90',
    '91', '92', '93', '94', '95', '96', '97', '98', '99',
]

priorities_list = [
    # '008', # готово
    # '032', # готово
    # '050', # готово
    '064',
    # '070',
    # '072',
    # '096',
    # '108',
    # '144',
    # '158',
    # '204',
    # '222',
    # '242',
    # '270',
    # '288',
    # '308',
    # '324',
    # '344',
    # '352',
    # '360',
    # '376',
    # '384',
    # '404',
    # '426',
    # '430',
    # '446',
    # '458',
    # '466',
    # '480',
    # '516',
    # '520',
    # '524',
    # '562',
    # '566',
    # '586',
    # '608',
    # '624',
    # '646',
    # '686',
    # '690',
    # '694',
    # '699',
    # '702',
    # '710',
    # '748',
    # '768',
    # '776',
    # '788',
    # '800',
    # '834',
    # '854',
    # '862',
    # '876',
]
ormCreateTable()
mac_map_main = MacMap()

countries_list = MacMap().countries()
countries = [i['Code'] for i in countries_list]
countries.sort()
for i_tn_ved2 in tn_ved_2:
    for i_reporter in priorities_list:  # приоритетные страны
        print(i_reporter)
        # при вводе ТН ВЭД 2 знака получаем JSON со всеми знаками ТН ВЭД длинной 6 знаков
        tn_ved6_data = MacMap.productsByKeyword(mac_map_main, i_reporter, i_tn_ved2)
        tn_ved6_list = [i['Code'] for i in tn_ved6_data]
        for i_tn_ved6 in tn_ved6_list:
            start_time = time.time()
            # При вводе ТН ВЭД 6 знаков получаем JSON со всеми знаками ТН ВЭД длинной 8-12 знаков
            tn_ved_all_json = MacMap.ntlcProduct(mac_map_main, i_reporter, i_tn_ved6)
            tn_ved_all_list = [i['Code'] for i in tn_ved_all_json]

            for i_tn_ved_all in tn_ved_all_list:
                # plan request creation
                i_obj = checkingQueryPlan(i_reporter, '643', i_tn_ved_all)
                # if i_obj:
                #
                #     mac_map_results = MacMapResults(i_obj.reporter, i_obj.partner, i_obj.tn_ved)
                #     if mac_map_results:
                #         custom_duties = mac_map_results.customDuties()
                #         customDutiesUpdate(i_obj.id, custom_duties)
                #         customDutiesLevelUpdate(i_obj.id, custom_duties)
                #
                #     ntm_measures = mac_map_results.ntmMeasures()
                #     if ntm_measures:
                #         ntmMeasuresUpdate(i_obj.id, ntm_measures)
                #         measuresUpdate(i_obj.id, ntm_measures)
                #         allMeasuresUpdate(i_obj.id, ntm_measures)
                #
                #     tradere_medy = mac_map_results.tradereMedy()
                #     if tradere_medy:
                #         tradeRemedyUpdate(i_obj.id, tradere_medy)
                #
                #     taxes = mac_map_results.taxes()
                #     if taxes:
                #         taxesUpdate(i_obj.id, taxes)
                # print("%s sec" % (time.time() - start_time))
