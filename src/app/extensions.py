from flask_sqlalchemy import SQLAlchemy


def register_extensions(app):
    db.init_app(app)


db = SQLAlchemy()
