from datetime import datetime

from flask import jsonify


def make(success: bool, message: str, data: object):
    return jsonify(
        {
            "data": data,
            "time": datetime.now(),
            "success" if success else "error": message,
            # "status": "success" if success else "error",
        }
    )


def success(msg: str, data: object = None):
    return make(True, msg, data)


def error(msg: str, data: object = None):
    return make(False, msg, data)
