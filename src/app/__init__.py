from flask import Flask

from app.core.blueprint import register_blueprints
from app.core.error import register_error_handler
from app.core.json import register_json_provider
from app.extensions import register_extensions
from app.settings import config


def create_app():
    app = Flask(__name__)

    # app.config.update(config)
    app.config.from_object(config)

    register_blueprints(app)
    register_extensions(app)
    register_error_handler(app)
    register_json_provider(app)
    return app
