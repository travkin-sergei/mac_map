import os
import logging

address_folder_full = os.path.dirname(os.path.abspath(__file__))
address = address_folder_full.split('\\')
for _ in range(3):
    del address[-1]
    address_log = '/'.join(address)


def log_connect():
    logging.basicConfig(
        level=logging.WARNING,
        filename=f"{address_log}/logger.log",
        format='%(asctime)s,%(msecs)d,%(name)s,%(levelname)s,%(message)s',
    )
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    result = logging.getLogger()  # "sqlalchemy.engine").setLevel(logging.INFO)
    return result


def logger_fun(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as error:
            result = f'def {func.__name__}: {error}'
            print(result)
            log_connect().error(result)

        return result

    return wrapper
