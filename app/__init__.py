from flask import Flask

from app.blueprints import register_blueprints
from app.core.auth import register_auth_handler
from app.core.error import register_error_handler
from app.core.resp import register_resp_handler
from app.extensions import register_extensions
from app.settings import basedir, config


def create_app():
    app = Flask(__name__)

    # app.config.update(config)
    app.instance_path = basedir
    app.config.from_object(config)

    register_blueprints(app)
    register_extensions(app)
    register_resp_handler(app)
    register_auth_handler(app)
    register_error_handler(app)
    return app


app = create_app()
