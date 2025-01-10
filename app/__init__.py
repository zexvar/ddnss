from flask import Flask

from .blueprints import register_blueprints
from .core import register_components
from .extensions import register_extensions
from .settings import BASEDIR, CONFIG


def create_app():
    app = Flask(__name__)

    app.instance_path = BASEDIR
    app.config.from_object(CONFIG)
    app.url_map.strict_slashes = False

    register_blueprints(app)
    register_extensions(app)
    register_components(app)
    return app


app = create_app()
