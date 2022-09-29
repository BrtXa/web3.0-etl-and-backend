from sanic import Blueprint

from app.api.example_blueprint import example_bp
from app.api.get_event_data_blueprint import get_event_data_bp
from app.api.test_login_blueprint import test_login_bp
from app.api.test_protected_blueprint import test_protected_bp

api = Blueprint.group(
    [
        example_bp,
        get_event_data_bp,
        test_login_bp,
        test_protected_bp,
    ]
)
