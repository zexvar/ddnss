from app.blueprints import Blueprint
from app.core.auth import Auth
from app.core.resp import Html

bp = Blueprint("index", __name__)


@bp.route("/")
@Auth.required
def index():
    return Html.render("index.jinja")
