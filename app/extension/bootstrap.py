from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()


def init(app):
    bootstrap.init_app(app)
