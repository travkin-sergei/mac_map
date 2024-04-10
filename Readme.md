# Получение данных по API MacMap.org
## Термины и определения
+ hash_address - hashSum256 от выбранных полей строки
+ hash_data - hashSum256 от всех полей строки
## Технология
+ python 3.12
+ requests
+ sqlalchemy

### Преобразование
```python
import re
def camelToSnake(data):
    """
    CamelCase is not allowed in the database
    :param data: dict where the keys are a CamelCase
    :return: dict where the keys are a camel snake_case
    """
    for old_key in data:
        for old_key in data:
            for old_key in data:
                new_key = re.sub(r'(?<!^)(?=[A-Z])', '_', old_key).lower()
        print(old_key, ';', new_key)
    return data
```

