from app.utils.auth import BasicAuth
from app.utils.peewee import FlaskDB

db = FlaskDB()
auth = BasicAuth()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


def init_auth(app):
    auth.init_app(app)


def register_extensions(app):
    init_db(app)
    init_auth(app)
