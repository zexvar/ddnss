from app.exts.sqlalchemy import db
from datetime import datetime


# 记录实体类型
class Record(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    host = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    ip = db.Column(db.String(100))
    key = db.Column(db.String(50))
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
