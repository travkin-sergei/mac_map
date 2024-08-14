from src.prod.site.class_site import Macmap

mac_map_main = Macmap()

countries_list = Macmap().countries()
countries = [i['Code'] for i in countries_list]


for i_reporter in countries:
    for i_partner in countries:
        if i_reporter == i_partner:
            continue
            list_code = MacMap.products(mac_map_main, i_reporter)
            print(f'i_reporter={i_reporter};list_code={list_code}')
exit()
