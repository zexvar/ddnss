from app.utils.peewee import PeeweeORM

orm = PeeweeORM()


def init_db(app):
    orm.init_app(app)
    with app.app_context():
        # Ensure models are imported to register them
        from app import models

        orm.create_all()


def register_extensions(app):
    init_db(app)
