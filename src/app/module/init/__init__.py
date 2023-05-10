import importlib
import os

from flask import Blueprint
from app.exts import db
from app.util import response

bp = Blueprint('database', __name__, url_prefix='/init')


@bp.route("/")
def init_db():
    entities = []
    for d in os.listdir('app/entity/'):
        if not d.endswith('__'):
            entity = importlib.import_module('app.entity.' + d.replace('.py', ''))
            entities.append(entity.__name__)
    db.create_all()
    return response.success("Operation succeed!", {'created': entities})
