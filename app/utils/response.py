from datetime import datetime

from flask import jsonify, render_template, request


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


def resp(html, rest):
    accept = request.headers.get("accept", "*/*")
    # html response
    if "text/html" in accept:
        return render_template(html)
    # json response
    else:
        return error(rest)
