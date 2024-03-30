import os
import logging

address_folder_full = os.path.dirname(os.path.abspath(__file__))
address = address_folder_full.split('\\')
for _ in range(3):
    del address[-1]
    address_log = '/'.join(address)


def logConect():
    logging.basicConfig(
        filename=f"{address_log}/logger.log",
        format='%(asctime)s,%(msecs)d,%(name)s,%(levelname)s,%(message)s',
        level=logging.WARNING
    )
    result = logging.getLogger()
    return result
