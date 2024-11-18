from flask import Flask
from peewee import Database, Model, Proxy
from playhouse.db_url import connect
from playhouse.flask_utils import PaginatedQuery as PeeweePaginatedQuery


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
            self._db_url = self._db_url or app.config.get("DATABASE") or app.config["DATABASE_URL"]
            if not self._db_url:
                raise ValueError("Missing required configuration data for " "database: DATABASE or DATABASE_URL.")
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

        print(f"Database create tables: {models}")
        self.database.create_tables(models)


class PaginatedQuery(PeeweePaginatedQuery):
    def __init__(self, query_or_model, page, page_size, page_show=5):
        super().__init__(query_or_model, page=page, paginate_by=page_size)

        page_max = self.get_page_count()
        if page > page_max:
            super().__init__(query_or_model, page=page_max, paginate_by=page_size)

        self.max = page_max
        self.size = page_size
        self.prev = page - 1 if page - 1 >= 1 else None
        self.next = page + 1 if page + 1 <= page_max else None
        self.range = self.get_page_range(page, page_max, show=page_show)
