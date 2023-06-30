import importlib
import os

from flask import Flask

from app.extensions import register_extensions
from app.utils.json import JSONProvider

config: dict


def create_app(config):
    globals()["config"] = config

    app = Flask(__name__)
    app.json = JSONProvider(app)
    app.config.update(config)

    register_blueprints(app)
    register_extensions(app)
    return app


def register_blueprints(app):
    dir_path = f"{app.name}/blueprints"  # app/blueprints/xxx
    mod_path = f"{app.name}.blueprints"  # app.blueprints.xxx
    for file in os.listdir(dir_path):
        if file.startswith("__"):
            continue
        mod_name = file[:-3] if file.endswith(".py") else file
        module = importlib.import_module(f"{mod_path}.{mod_name}")
        blueprint = getattr(module, "bp")
        bp_prefix = blueprint.url_prefix
        if bp_prefix is None:
            bp_prefix = f"/{blueprint.name}"
        app.register_blueprint(blueprint, url_prefix=bp_prefix)
        print(f"Register blueprint: {module.__name__} {bp_prefix}")
