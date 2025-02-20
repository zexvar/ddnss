from flask import request

from app.blueprints import Blueprint
from app.core.auth import Auth
from app.core.resp import Html
from app.models import History
from app.utils import peewee

bp = Blueprint("history", __name__, url_prefix="/history")


@bp.before_request
@Auth.required
def before():
    pass


@bp.route("/")
def index():
    page = request.values.get("page", 1, type=int)
    limit = request.values.get("limit", 20, type=int)
    print(request.values)
    import logging

    # 打印生成的查询语句
    logger = logging.getLogger("peewee")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    query = History.select(
        History.id,
        History.name,
        History.type,
        History.content,
        History.success,
        History.create_time,
    ).order_by(History.create_time.desc())

    result = peewee.OffsetPagination(query, page, limit)
    return Html.render(
        "history.jinja",
        items=result.items,
        pagination=result.pagination,
        status=200,
    )
