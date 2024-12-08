from dataclasses import asdict, dataclass
from datetime import datetime

from peewee import *

from app.extensions import orm


@dataclass(init=False)
class Base(Model):
    create_time: datetime = DateTimeField(default=datetime.now)
    update_time: datetime = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.update_time = datetime.now()
        return super().save(*args, **kwargs)

    @property
    def dict(self):
        return asdict(self)

    class Meta:
        database = orm.database


@dataclass(init=False)
class Zone(Base):
    id: str = CharField(primary_key=True)
    name: str = CharField(index=True)


@dataclass(init=False)
class Record(Base):
    id: str = CharField(primary_key=True)
    name: str = CharField()
    type: str = CharField()
    content: str = CharField()
    zone: Zone = ForeignKeyField(Zone, backref="records")

    class Meta:
        database = orm.database
        indexes = ((("name", "type"), True),)


@dataclass(init=False)
class History(Base):
    id: int = BigAutoField(primary_key=True)
    name: str = CharField()
    type: str = CharField()
    content: str = CharField()
    success: bool = BooleanField()
    record: Record = ForeignKeyField(Record, backref="histories")
