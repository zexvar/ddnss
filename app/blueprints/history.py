from flask import redirect, render_template, request, url_for

from app.blueprints import Blueprint
from app.models import History, PaginatedQuery

bp = Blueprint("history", __name__, url_prefix="/history")


@bp.route("/")
def index():
    return redirect(url_for("history.page_view", page=1))


@bp.route("/view")
def page_view():
    # 分页显示
    page = max(request.values.get("page", 1, type=int), 1)
    page_size = 20

    pagination = PaginatedQuery(
        History.select().order_by(History.create_time.desc()),
        paginate_by=page_size,
        page=page,
    )

    page_max = pagination.get_page_count()
    page_prev = page - 1 if page - 1 >= 1 else False
    page_next = page + 1 if page + 1 <= page_max else False
    page_range = pagination.get_page_range(page, page_max, show=11)
    object_list = pagination.get_object_list()

    return render_template(
        "history.jinja",
        page=page,
        page_max=page_max,
        page_prev=page_prev,
        page_next=page_next,
        page_range=page_range,
        object_list=object_list,
    )
