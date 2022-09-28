from sanic.response import json
from sanic_openapi import doc, openapi2_blueprint

from app import create_app
from app.api import api
from config import SanicConfig, MongoDBConfig
from utils.logger_utils import logging_basic_config

app = create_app(SanicConfig, MongoDBConfig)
app.blueprint(openapi2_blueprint)


@app.route("/hello-world", methods={"GET", "POST"})
@doc.tag("hello_world")
@doc.summary("Hello, Sanic!")
async def hello_world(request):
    return json({"Hello": "World"})


if __name__ == "__main__":
    app.blueprint(api)
    app.run(**app.config["RUN_SETTING"])
    logging_basic_config()
