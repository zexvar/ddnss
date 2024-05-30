from playhouse.flask_utils import FlaskDB as PeeweeFlaskDB
from playhouse.flask_utils import PaginatedQuery as PeeweePaginatedQuery


def subclasses(cls):
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in subclasses(c)])


class FlaskDB(PeeweeFlaskDB):
    def create_all(self):
        self.database.create_tables(subclasses(self.Model))


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
