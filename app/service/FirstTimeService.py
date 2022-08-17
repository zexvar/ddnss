import importlib
import os

from flask import Blueprint, current_app, jsonify
from app.exts.db import db

first_bp = Blueprint('first_bp', __name__)

app = current_app


@first_bp.route("/init")
def init_db():
    entities = []
    for d in os.listdir('app/entity/'):
        if not d.endswith('__'):
            entity = importlib.import_module('app.entity.' + d.replace('.py', ''))
            entities.append(entity.__name__)
    db.create_all(app=app)
    return jsonify({'code': 0, 'msg': 'Operation succeeded!', 'created': entities})
