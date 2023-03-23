from dataclasses import dataclass

from app.exts import db
from datetime import datetime


# record变更历史
@dataclass
class History(db.Model):
    __table_args__ = {'extend_existing': True}
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip: str = db.Column(db.String(100))
    host: str = db.Column(db.String(50))
    status: bool = db.Column(db.Boolean)
    create_time: str = db.Column(db.DateTime, default=datetime.now)
