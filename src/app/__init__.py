import yaml
from flask import Flask

from app import extensions

config = yaml.load(open('config.yml', 'r'), Loader=yaml.FullLoader)


def create_app():
    app = Flask(__name__)
    app.config.update(config)
    extensions.init(app)
    return app
