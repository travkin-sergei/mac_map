# Получение данных по API MacMap.org

## Технология
+ python 3.12
+ requests
+ sqlalchemy

### преобразование
```python
import re
def camel_to_snake(data: dict):
    """
    CamelCase is not allowed in the database
    :param data: dict where the keys are a CamelCase
    :return: dict where the keys are a camel snake_case
    """

    for old_key in data:
        new_key = re.sub(r'(?<!^)(?=[A-Z])', '_', old_key).lower()
        print(old_key,';',new_key)
    return data

```