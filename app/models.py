from dataclasses import dataclass
from datetime import datetime

from peewee import *
from playhouse.flask_utils import *

db = FlaskDB()


@dataclass(init=False)
class Base(db.Model):
    __abstract__ = True
    create_time: datetime = DateTimeField(default=datetime.now)
    update_time: datetime = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.update_time = datetime.now()
        return super(Base, self).save(*args, **kwargs)


@dataclass(init=False)
class Record(Base):
    id: str = CharField(max_length=50, primary_key=True)
    host: str = CharField(max_length=100)
    name: str = CharField(max_length=100)
    type: str = CharField(max_length=10)
    content: str = CharField(max_length=100)

    class Meta:
        indexes = ((("host", "type"), True),)


@dataclass(init=False)
class History(Base):
    id: int = BigAutoField(primary_key=True)
    host: str = CharField(max_length=100)
    name: str = CharField(max_length=100)
    type: str = CharField(max_length=10)
    content: str = CharField(max_length=100)
    status: bool = BooleanField()
