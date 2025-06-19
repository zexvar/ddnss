from functools import wraps

from flask import Flask, redirect, request, session

from .resp import Html, Rest


class Auth:
    _token_key = "token"
    _session_key = "session"

    @classmethod
    def init_app(
        cls,
        app: Flask,
        token=None,
        username=None,
        password=None,
    ):
        cls._token = token or app.config.get("AUTH_TOKEN")
        cls._username = username or app.config.get("AUTH_USERNAME")
        cls._password = password or app.config.get("AUTH_PASSWORD")

        if not cls._username:
            raise ValueError("Missing required `AUTH_USERNAME`")
        if not cls._password:
            raise ValueError("Missing required `AUTH_PASSWORD`")

        def login():
            if request.method == "GET":
                returnUrl = request.values.get("returnUrl", "/")
                return Html.render("/login.jinja", returnUrl=returnUrl)
            else:
                username = request.values.get("username")
                password = request.values.get("password")
                if username == cls._username and password == cls._password:
                    session[cls._session_key] = username
                    return Rest.success("Login success")
                return Rest.error("Invalid username or password")

        def logout():
            session.pop(cls._session_key, None)
            return Html.make(redirect("/login"))

        app.add_url_rule("/login/", view_func=login, methods=["POST", "GET"])
        app.add_url_rule("/logout/", view_func=logout, methods=["POST", "GET"])

    @classmethod
    def token(cls, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = (
                request.headers.get(cls._token_key)
                or request.args.get(cls._token_key)
                or request.cookies.get(cls._token_key)
            )
            if cls._token and token != cls._token:
                return Rest.error("Invalid or missing token", status=401)
            return f(*args, **kwargs)

        return decorated

    @classmethod
    def session(cls, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if cls._session_key not in session:
                return Html.make(redirect(f"/login?returnUrl={request.path}"))
            return f(*args, **kwargs)

        return decorated


def register_auth_handler(app):
    Auth.init_app(app)
