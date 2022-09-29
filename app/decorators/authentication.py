from sanic import text
from sanic.request import Request
from functools import wraps
import jwt

from config import SanicConfig


def check_token(request: Request):
    token = request.token

    if not token:
        return False

    try:
        jwt_ = jwt.decode(token, SanicConfig.SECRET_KEY, algorithms=["HS256"])
        if jwt_["role"] == "admin":
            return True

    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)

            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return text("You are unauthorized.", 401)

        return decorated_function

    return decorator(wrapped)
