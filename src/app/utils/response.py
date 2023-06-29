from datetime import datetime

from flask import jsonify


def make(success: bool, message: str, data: object):
    return jsonify(
        {
            "success": success,
            "message": message,
            "data": data,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


def success(msg: str, data: object = None):
    return make(True, msg, data)


def error(msg: str, data: object = None):
    return make(False, msg, data)
