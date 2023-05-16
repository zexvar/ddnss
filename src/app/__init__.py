from flask import Flask

from app import extensions


def create_app():
    app = Flask(__name__)
    extensions.init(app)
    return app
