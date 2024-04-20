from app.utils.peewee import FlaskDB

db = FlaskDB()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


def register_extensions(app):
    init_db(app)
