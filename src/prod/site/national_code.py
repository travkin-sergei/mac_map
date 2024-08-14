"""
Получение списка стран и их ТН ВЭД максимальной доступной версии h6
подробнее на сайте - https://www.macmap.org/en/resources/product-search?reporter=004&keyword=010110&level=false
"""

from src.prod.site.class_site import Macmap
from src.prod.site.orm import ormCreateTable, insert_products
from src.test.translated import translated_text

priorities_list = [
    # '008','040','050', '056','070', '072', '100', '108', '156', '204',
     '222', '233',
    #'242', '246', '251', '270',
    # '288', '324', '344', '384', '404', '426', '428', '430', '440', '442', '446', '466', '480', '490', '516', '520',
    # '524', '528', '562', '566', '585', '586', '598', '616', '624', '642', '646', '686', '694', '699', '702', '703',
    # '710', '724', '748', '768', '788', '792', '800', '834', '854', '876', '895',
]

ormCreateTable()
mac_map = Macmap()

# country_list = [i['Code'] for i in mac_map.countries()]
for i_country in priorities_list:
    try:
        tn_ved_list = mac_map.products(i_country)
        for i_tn_ved in tn_ved_list:
            i_tn_ved['language'] = translated_text(i_tn_ved.get('Name'))[0]
            i_tn_ved['name_rus'] = translated_text(i_tn_ved.get('Name'))[1]
            insert_products(i_tn_ved, i_country)
    except:
        print(f'Ошибка: Страна = {i_country}, ТН ВЭД = {i_tn_ved}')
