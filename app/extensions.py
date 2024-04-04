from app.models import Base, db


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.database.create_tables(Base.__subclasses__())


def register_extensions(app):
    init_db(app)
