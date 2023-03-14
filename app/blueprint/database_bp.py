import importlib
import os

from flask import Blueprint, jsonify
from app.extension.sqlalchemy import db
bp = Blueprint('database', __name__)


@bp.route("/init")
def init_db():
    entities = []
    for d in os.listdir('app/entity/'):
        if not d.endswith('__'):
            entity = importlib.import_module('app.entity.' + d.replace('.py', ''))
            entities.append(entity.__name__)
    db.create_all()
    return jsonify({'code': 0, 'msg': 'Operation succeeded!', 'created': entities})
