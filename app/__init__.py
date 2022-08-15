import yaml
from flask import Flask
from app.exts import bp, db


def create_app():
    app = Flask(__name__, static_url_path='')
    app.config.update(yaml.full_load(open('app/config/config.yaml', 'r')))
    db.init_app(app)
    bp.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='::')
