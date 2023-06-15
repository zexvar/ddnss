from datetime import datetime

from flask import jsonify


def make(code: int, msg: str, data: object):
    return jsonify(
        {
            "code": code,
            "msg": msg,
            "data": data,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


def success(msg: str, data: object):
    return make(0, msg, data)


def error(msg: str):
    return make(-1, msg, None)
