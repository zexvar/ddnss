from flask import Blueprint, current_app, jsonify
from app.exts.db import db

record_bp = Blueprint('record_bp', __name__)


class RecordService:
    app = current_app
