import jwt
from sanic import Blueprint, text
from sanic_openapi.openapi2 import doc
from config import SanicConfig

test_login_bp: Blueprint = Blueprint(name="test_get_token", url_prefix="/login")


@test_login_bp.route("/post-login", methods={"POST"})
@doc.tag("test")
async def do_login(request):
    token = jwt.encode({}, SanicConfig.SECRET_KEY)
    return text(token)
