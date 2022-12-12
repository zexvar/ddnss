from flask_sqlalchemy import SQLAlchemy
import pymysql

db = SQLAlchemy()


def init(app):
    db.init_app(app)
