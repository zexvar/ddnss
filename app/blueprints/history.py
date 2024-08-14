from flask import request

from app.blueprints import Blueprint, new
from app.core.auth import Auth
from app.core.resp import Html
from app.models import History
from app.utils import peewee

bp = new(Blueprint("history", __name__, url_prefix="/history"))


@bp.before_request
@Auth.required
def before():
    pass


@bp.route("/")
def index():
    page = max(request.values.get("page", 1, type=int), 1)
    page_size = request.values.get("page_size", 20, type=int)

    pagination = peewee.PaginatedQuery(
        History.select().order_by(History.create_time.desc()),
        page_size=page_size,
        page=page,
    )

    return Html.render(
        "history.jinja",
        pagination=pagination,
        object_list=pagination.get_object_list(),
        status=400,
    )
