from app.exts.db import db
from datetime import datetime


# 记录实体类型
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    host = db.Column(db.String(50), unique=True)
    ip = db.Column(db.String(100))
    key = db.Column(db.String(30))
    mac = db.Column(db.String(20))
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, host, ip, key):
        self.host = host
        self.key = key
        self.ip = ip
