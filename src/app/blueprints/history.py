from flask import Blueprint, render_template, request

from app.models import History

bp = Blueprint("history", __name__)


@bp.route("/latest")
def history_latest():
    history_list = History.query.order_by(History.create_time.desc()).limit(100).all()
    return render_template(
        "history.html", title="Last 100 Records", history_list=history_list
    )


@bp.route("/")
def history_page():
    # 分页显示
    page = request.args.get("page", 1, type=int)
    page = 1 if page <= 0 else page
    history_list = History.query.order_by(History.create_time.desc()).paginate(
        page=page, per_page=100
    )
    return render_template(
        "history.html", title="Record List", history_list=history_list
    )
