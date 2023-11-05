from flask import render_template, request

from app.blueprints import Blueprint
from app.models import History

bp = Blueprint("history", __name__)


@bp.route("/latest")
def history_latest():
    history_list = History.query.order_by(History.create_time.desc()).limit(100).all()
    return render_template("history.html", title="Latest records", history_list=history_list)


@bp.route("/")
def history_page():
    # 分页显示
    page = request.values.get("page", 1, type=int)
    page = 1 if page <= 0 else page
    history_list = History.query.order_by(History.create_time.desc()).paginate(page=page, per_page=100)
    return render_template("history.html", title=f"Paginated view", history_list=history_list)
