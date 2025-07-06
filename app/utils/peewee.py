import math
from dataclasses import dataclass

from flask import Flask
from peewee import Database, Model, Proxy, SelectQuery
from playhouse.db_url import connect

from app.core.log import logger


def subclasses(clazz):
    result = []

    def collect_subclasses(cls):
        for subclass in cls.__subclasses__():
            if subclass not in result:
                result.append(subclass)
                collect_subclasses(subclass)

    collect_subclasses(clazz)
    return result


class PeeweeORM:
    def __init__(self, app=None, database=None, connect_url=None):
        self.database = Proxy()
        self._db = database
        self._db_url: str = connect_url
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app
        if not self._db:
            self._db_url = (
                self._db_url or app.config.get("DATABASE") or app.config["DATABASE_URL"]
            )
            if not self._db_url:
                raise ValueError(
                    "Missing required configuration data for "
                    "database: DATABASE or DATABASE_URL."
                )
            self._db = connect(self._db_url)

        if isinstance(self._db, Database):
            self.database.initialize(self._db)
        elif isinstance(self._db, Proxy):
            self.database = self._db
        else:
            raise RuntimeError("Database initialize failed.")

        app.before_request(self.connect_db)
        app.teardown_request(self.close_db)

    def connect_db(self):
        self.database.connect()

    def close_db(self, exc):
        if not self.database.is_closed():
            self.database.close()

    def create_all(self, ignore_base_model=True):
        # Filter models associated with the current database
        models = [
            model
            for model in subclasses(Model)
            if model._meta.database == self.database
            and (not ignore_base_model or not model.__name__.startswith("Base"))
        ]
        logger.debug(f" * Database create tables: {models}")
        self.database.create_tables(models)


@dataclass
class Pagination:
    prev: int = None
    curr: int = None
    next: int = None
    count: int = None
    limit: int = None


class OffsetPagination:
    query: SelectQuery
    pagination: Pagination = None

    def __init__(
        self,
        query: SelectQuery,
        page: int = 1,
        limit: int = 10,
    ):
        self.query = query

        page = max(1, page)
        count = math.ceil(query.count() / limit)

        self.pagination = Pagination(
            curr=page,
            count=count,
            limit=limit,
            prev=page - 1 if page - 1 >= 1 else None,
            next=page + 1 if page + 1 <= count else None,
        )

    @property
    def items(self):
        return self.get_object_list() or []

    def get_object_list(self):
        if self.pagination.curr > self.pagination.count:
            return None
        return self.query.paginate(self.pagination.curr, self.pagination.limit)
