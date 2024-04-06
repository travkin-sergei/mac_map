import sys
import time
import asyncio

from src.prod.site.orm import (
    MacMap,
    MacMapResults,
    customDutiesUpdate,
    customDutiesLevelUpdate,
    ntmMeasuresUpdate,
    measuresUpdate,
    allMeasuresUpdate,
    tradeRemedyUpdate,
    taxesUpdate,
    checkingQueryPlan,
    getQueryPlan,
    updateQueryPlanActive,
    log,
)


def parser():
    tn_ved_2 = (
        '01', '02', '03', '04', '05', '06', '07', '08', '09',
        '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
        '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
        '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
        '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
        '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
        '60', '61', '62', '63', '64', '65', '66', '67', '68', '69',
        '70', '71', '72', '73', '74', '75', '76', '77', '78', '79',
        '80', '81', '82', '83', '84', '85', '86', '87', '88', '89',
        '90', '91', '92', '93', '94', '95', '96', '97', '98',
    )
    mac_map_main = MacMap()

    countries_list = MacMap().countries()
    countries = [i['Code'] for i in countries_list]
    for i_tn_ved2 in tn_ved_2:
        for i_reporter in countries:
            for i_partner in countries:
                if i_reporter == i_partner:
                    continue
                tn_ved6_data = MacMap.products_by_keyword(mac_map_main, i_reporter, i_tn_ved2)
                tn_ved6_list = [i['Code'] for i in tn_ved6_data]
                for i_tn_ved6 in tn_ved6_list:
                    start_time = time.time()
                    tn_ved_all_json = MacMap.ntlc_product(mac_map_main, i_reporter, i_tn_ved6)
                    tn_ved_all_list = [i['Code'] for i in tn_ved_all_json]
                    for i_tn_ved_all in tn_ved_all_list:
                        # plan request creation
                        i_obj = checkingQueryPlan(i_reporter, i_partner, i_tn_ved_all)
                        if i_obj:
                            mac_map_results = MacMapResults(i_obj.reporter, i_obj.partner, i_obj.tn_ved)
                            if mac_map_results:
                                customduties = mac_map_results.customduties()
                                customDutiesUpdate(i_obj.id, customduties)
                                customDutiesLevelUpdate(i_obj.id, customduties)

                            ntm_measures = mac_map_results.ntm_measures()
                            if ntm_measures:
                                ntmMeasuresUpdate(i_obj.id, ntm_measures)
                                measuresUpdate(i_obj.id, ntm_measures)
                                allMeasuresUpdate(i_obj.id, ntm_measures)

                            traderemedy = mac_map_results.traderemedy()
                            if traderemedy:
                                tradeRemedyUpdate(i_obj.id, traderemedy)

                            taxes = mac_map_results.taxes()
                            if taxes:
                                taxesUpdate(i_obj.id, taxes)
                        print("%s sec" % (time.time() - start_time))
