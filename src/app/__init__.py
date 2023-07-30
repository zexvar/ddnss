from flask import Flask

from app.core.blueprint import register_blueprints
from app.core.error import register_error_handler
from app.core.json import register_json_provider
from app.extensions import register_extensions

app_config: dict


def create_app():
    app = Flask(__name__)

    register_config(app)
    register_extensions(app)
    register_blueprints(app)
    register_error_handler(app)
    register_json_provider(app)
    return app


def register_config(app):
    try:
        import yaml

        config = yaml.full_load(open("config.yml"))
    except IOError:
        # use default config
        # config = {"SQLALCHEMY_TRACK_MODIFICATIONS": False, "SQLALCHEMY_DATABASE_URI": "sqlite:///data/app.db"}
        config = {"SQLALCHEMY_DATABASE_URI": "sqlite:///data/app.db"}

    global app_config
    app_config = config

    app.config.update(config)
