from app.exts.db import db
from datetime import datetime


# record变更历史
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(100))
    host = db.Column(db.String(50))
    status = db.Column(db.Boolean)
    create_time = db.Column(db.DateTime, default=datetime.now)

