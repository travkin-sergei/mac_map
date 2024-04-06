import time

from src.prod.site.orm import MacMap, ormCreateTable, updateCountry, updateProducts

ddd = [
    "246", "410", "340", "032", "418", "660", "222", "070", "188", "428", "400", "184", "036", "266", "120",
    "100", "231", "854", "152", "438", "533", "050", "699", "352", "426", "060", "324", "226", "028", "218", "076",
    "332", "196", "052", "132", "012", "530", "174", "156", "270", "288", "140", "044", "008", "064", "381", "292",
    "364", "384", "233", "818", "203", "208", "296", "124", "624", "328", "414", "251", "276", "268", "262", "404",
    "434", "148", "031", "136", "212", "388", "360", "051", "348", "192", "392", "056", "204", "300", "084", "308",
    "024", "004", "191", "116", "320", "344", "895", "214", "178", "398", "242", "040", "417", "072", "180", "430",
    "376", "096", "372", "048", "258", "108", "170", "112", "422", "748", "068",
]


def main():
    ormCreateTable()

    # updating directories
    countries = MacMap().countries()

    if countries:
        for i_data in countries:
            updateCountry(i_data)
    country_list = [i['Code'] for i in countries]
    for i_country in country_list:
        if i_country not in ddd:
            products = MacMap().products(i_country)
            time.sleep(5)
            if products:
                for i_data in products:
                    updateProducts(i_data, i_country)


# Все что ниже удалить если включать в Airflow
if __name__ == '__main__':
    main()
else:
    raise SystemExit("Это не библиотека")
