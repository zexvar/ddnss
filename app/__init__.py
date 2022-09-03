from flask import Flask

from app.exts import bp, db, config, bootstrap


def create_app():
    app = Flask(__name__, static_url_path='')
    bootstrap.init_app(app)
    config.init_app(app)
    db.init_app(app)
    bp.init_app(app)
    return app
