import logging
from sanic import Sanic


def create_app(*config_cls) -> Sanic:
    sanic_app: Sanic = Sanic(__name__)

    for config in config_cls:
        sanic_app.config.update_config(config)

    return sanic_app
