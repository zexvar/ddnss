from flask import Flask

from app.core.blueprint import register_blueprints
from app.core.json import register_json_provider
from app.extensions import register_extensions

config: dict


def create_app(config):
    globals()["config"] = config

    app = Flask(__name__)
    app.config.update(config)

    register_extensions(app)
    register_blueprints(app)
    register_json_provider(app)
    return app
