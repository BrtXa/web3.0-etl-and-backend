from sanic import Blueprint

from app.api.example_blueprint import example_bp
from app.api.get_event_data_blueprint import get_event_data_bp

api = Blueprint.group(
    [
        example_bp,
        get_event_data_bp,
    ]
)
