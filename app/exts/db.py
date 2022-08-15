from flask_sqlalchemy import SQLAlchemy
import pymysql

db = SQLAlchemy()


def init_app(app):
    global db
    db.init_app(app)
