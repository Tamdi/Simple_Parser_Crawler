import logging

logging.basicConfig(
    level=logging.INFO,
    format='{"app_name": "torgi_erg_collector", "time":"%(asctime)s", "name": "%(name)s", '
           '"level": "%(levelname)s", "msg": "%(message)s"}'
)


def get_logger(name: str):
    return logging.getLogger(name)