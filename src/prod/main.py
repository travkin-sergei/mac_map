from src.prod.site.orm import MacMap, MacMapResults, ormCreateTable, updateCountry


def main():
    ormCreateTable()

    # updating directories
    countries = MacMap().countries()

    if countries:
        for i_data in countries:
            updateCountry(i_data)
        print('Справочник стран обновлен')
    else:
        print('Справочник стран не обновлен')


# Все что ниже удалить если включать в Airflow
if __name__ == '__main__':
    main()
else:
    raise SystemExit("Это не библиотека")
