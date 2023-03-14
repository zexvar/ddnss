import yaml
from flask import Flask

from app import util
from app.extension import sqlalchemy, blueprint, bootstrap


def create_app():
    app = Flask(__name__)
    app.config.update(yaml.full_load(open('config.yaml', 'r')))
    sqlalchemy.init(app)
    blueprint.init(app)
    bootstrap.init(app)
    util.init(app)
    return app
