from app.exts.db import db
from datetime import datetime


# record变更历史
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(100))
    host = db.Column(db.String(50))
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, host, ip):
        self.host = host
        self.ip = ip
