import logging


def logging_basic_config():
    # format = "%(asctime)s [%(levelname)s]: %(name)s - %(message)s"
    format = "[%(asctime)s] [%(levelname)s] %(message)s (%(name)s)"
    logging.basicConfig(format=format, level=logging.INFO)
