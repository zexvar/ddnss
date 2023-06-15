from dataclasses import dataclass
from datetime import datetime

from app.extensions import db


# 记录实体类型
@dataclass
class Record(db.Model):
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.String(50), primary_key=True)
    host = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    ip = db.Column(db.String(100))
    key = db.Column(db.String(50))
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


# record变更历史
@dataclass
class History(db.Model):
    __table_args__ = {"extend_existing": True}
    id: int = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    ip: str = db.Column(db.String(100))
    host: str = db.Column(db.String(50))
    status: bool = db.Column(db.Boolean)
    create_time: str = db.Column(db.DateTime, default=datetime.now)
