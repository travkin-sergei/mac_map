from src.prod.site.orm import MacMap

data = MacMap()
year = data.get_tr_years(MacMap(), '004')

print(year)
