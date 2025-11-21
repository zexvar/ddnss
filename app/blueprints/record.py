from flask import Blueprint, request

from app.core.auth import Auth
from app.core.resp import Html
from app.models import Record
from app.utils import peewee

bp = Blueprint("record", __name__, url_prefix="/record")


@bp.route("/")
@Auth.session
def index():
    page = request.values.get("page", 1, type=int)
    limit = request.values.get("limit", 10, type=int)
    query = Record.select(
        Record.id,
        Record.name,
        Record.type,
        Record.content,
        Record.create_time,
    ).order_by(Record.create_time.desc())

    result = peewee.OffsetPagination(query, page, limit)

    return Html.render(
        "record.jinja",
        url="/record",
        items=result.items,
        pagination=result.pagination,
        status=200,
    )
