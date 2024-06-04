from flask import render_template, request

from app.blueprints import Blueprint, new
from app.extensions import auth
from app.models import History
from app.utils import peewee

bp = new(Blueprint("history", __name__, url_prefix="/history"))


@bp.before_request
@auth.reqired
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

    return render_template(
        "history.jinja",
        pagination=pagination,
        object_list=pagination.get_object_list(),
    )
