from flask import Flask

from app import exts


def create_app():
    app = Flask(__name__)
    exts.init(app)
    return app
