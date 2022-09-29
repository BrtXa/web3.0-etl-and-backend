from sanic import Blueprint
from sanic.response import json

example_bp = Blueprint("example_blueprint", url_prefix="/example")


@example_bp.route("/")
async def bp_root(request):
    return json({"example": "blueprint"})
