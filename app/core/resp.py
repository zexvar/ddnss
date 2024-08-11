from datetime import date, datetime

from flask import Flask, Response, jsonify, make_response, render_template, request


class Rest(Response):
    @classmethod
    def make(cls, success, message, data=None, status=None, headers=None):
        content = {"data": data, "time": datetime.now(), "success" if success else "error": message}
        return make_response(jsonify(content), status, headers)

    @classmethod
    def success(cls, message, data=None, status=None, headers=None):
        return cls.make(True, message, data, status, headers)

    @classmethod
    def error(cls, message, data=None, status=None, headers=None):
        return cls.make(False, message, data, status, headers)


class Html(Response):
    @classmethod
    def make(cls, content, status=None):
        return make_response(content, status)

    @classmethod
    def render(cls, template, context=None, status=None):
        return cls.make(render_template(template, **(context or {})), status)


def response(rest: Response, html: Response):
    """
    Return html or rest by `accept header`.
    """
    accept = request.headers.get("accept", "*/*")
    return html if "text/html" in accept else rest


def register_resp_handler(app: Flask):
    from flask.json.provider import DefaultJSONProvider

    class JSONProvider(DefaultJSONProvider):
        def default(self, o):
            if isinstance(o, date) or isinstance(o, datetime):
                return o.strftime("%Y-%m-%d %H:%M:%S")
            return super().default(o)

    app.json = JSONProvider(app)
    app.response_class = Response
