from datetime import date, datetime

from flask import Flask, Response, jsonify, render_template, request


def register_resp_handler(app: Flask):
    from flask.json.provider import DefaultJSONProvider

    class JSONProvider(DefaultJSONProvider):
        def default(self, o):
            if isinstance(o, date) or isinstance(o, datetime):
                return o.strftime("%Y-%m-%d %H:%M:%S")
            return super().default(o)

    app.json = JSONProvider(app)


class Rest(Response):
    def __new__(self, success, message, data=None, status=None) -> None:
        content = {"data": data, "time": datetime.now(), "success" if success else "error": message}
        return Response(jsonify(content), status)

    @classmethod
    def success(cls, msg, data=None):
        return cls(True, msg, data)

    @classmethod
    def error(cls, msg, data=None, status=None):
        return cls(False, msg, data, status)


class Html(Response):
    def __new__(self, template, context=None, status=None) -> None:
        content = render_template(template, **(context or {}))
        return Response(content, status)

    @classmethod
    def success(cls, template, context=None) -> None:
        return cls(template, context)

    @classmethod
    def error(cls, template, context=None, status=None) -> None:
        return cls(template, context, status)


def response(rest: Response, html: Response):
    """
    Return html or rest by `accept header`.
    """
    accept = request.headers.get("accept", "*/*")
    return html if "text/html" in accept else rest
