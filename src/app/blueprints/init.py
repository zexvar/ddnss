import importlib

import flask_sqlalchemy
from flask import Blueprint, current_app
from app.extensions import db
from app.utils import response

bp = Blueprint('init', __name__)


@bp.route("/db")
def init_db():
    model_list = []
    models = importlib.import_module(f'{current_app.name}.models')
    for model_name in dir(models):
        model = getattr(models, model_name)
        if isinstance(model, flask_sqlalchemy.model.DefaultMeta):
            model_list.append(model_name)
    db.create_all()
    return response.success("Operation succeed!", {'created': model_list})
