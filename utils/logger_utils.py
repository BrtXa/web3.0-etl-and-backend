import logging


def logging_basic_config():
    format = "%(asctime)s: %(name)s - [%(levelname)s]:%(message)s"
    logging.basicConfig(format=format, level=logging.INFO)
