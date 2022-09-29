import jwt
from sanic import Blueprint, text
from sanic_openapi.openapi2 import doc
from app.decorators.auth import protected

test_protected_bp: Blueprint = Blueprint(name="test_use_token", url_prefix="/login")


@test_protected_bp.route("/get-login", methods={"GET"})
@doc.tag("test")
@protected
async def secret(request):
    return text("This is a protected blueprint.")
