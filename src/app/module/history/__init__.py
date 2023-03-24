from flask import Blueprint, request, render_template
from sqlalchemy import desc

from app.entity.history import History

bp = Blueprint('history', __name__, url_prefix='/history')


@bp.route('/')
def history_top100():
    # 分页显示
    page = request.args.get('page', 1, type=int)
    history_list = History.query.order_by(desc(History.create_time)).limit(100).all()
    return render_template('history.html', history_list=history_list)
