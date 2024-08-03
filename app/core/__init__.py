from .auth import register_auth_handler
from .error import register_error_handler
from .resp import register_resp_handler


def register_components(app):
    register_resp_handler(app)
    register_auth_handler(app)
    register_error_handler(app)
