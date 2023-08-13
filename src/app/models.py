from dataclasses import dataclass
from datetime import datetime

from app.extensions import db


@dataclass(init=False)
class Base(db.Model):
    __abstract__ = True
    create_time: datetime = db.Column(db.DateTime, default=datetime.now)
    update_time: datetime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


@dataclass(init=False)
class Record(Base):
    __table_args__ = (
        # db.Index("index_host_type", "host", "type"),
        db.UniqueConstraint("host", "type", name="unique_host_type"),
        {"extend_existing": True},
    )
    id: str = db.Column(db.String(50), primary_key=True)
    host: str = db.Column(db.String(100))
    name: str = db.Column(db.String(100))
    type: str = db.Column(db.String(10))
    content: str = db.Column(db.String(100))


@dataclass(init=False)
class History(Base):
    __table_args__ = {"extend_existing": True}
    id: int = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    host: str = db.Column(db.String(100))
    name: str = db.Column(db.String(100))
    type: str = db.Column(db.String(10))
    content: str = db.Column(db.String(100))
    status: bool = db.Column(db.Boolean)
