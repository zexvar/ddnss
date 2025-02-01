from functools import wraps

from flask import Flask, redirect, request

from .resp import Html, Rest, response


class Auth:
    @classmethod
    def init_app(
        cls,
        app: Flask,
        enable=None,
        username=None,
        password=None,
        enable_builtin_route=True,
    ):
        cls._app = app
        cls._enable = enable
        cls._username = username
        cls._password = password
        cls._builtin_route = enable_builtin_route

        if cls._enable is None:
            cls._enable = app.config.get("AUTH_ENABLE", False)

        if cls._enable:
            cls._username = app.config.get("AUTH_USERNAME", None)
            if cls._username is None or len(cls._username) == 0:
                raise ValueError("Missing required configuration for AUTH_USERNAME")

            cls._password = app.config.get("AUTH_PASSWORD", None)
            if cls._password is None or len(cls._password) == 0:
                raise ValueError("Missing required configuration for AUTH_PASSWORD")

            import base64

            b64auth = base64.b64encode(f"{cls._username}:{cls._password}".encode())
            cls._authorization = f"Basic {b64auth.decode()}"

            if cls._builtin_route:
                cls.register_builtin_route()

    @classmethod
    def register_builtin_route(cls):
        app = cls._app

        # Add route for login
        @app.route("/login/", methods=["GET", "POST"])
        def login():
            if request.method == "GET":
                returnUrl = request.values.get("returnUrl", "/")
                return Html.render("/login.jinja", returnUrl=returnUrl)
            else:
                if (
                    request.values.get("username") == cls._username
                    and request.values.get("password") == cls._password
                ):
                    resp = Rest.success("login success!")
                    resp.set_cookie("authorization", cls._authorization, max_age=3600)
                    return resp
                else:
                    return Rest.error("Username or password error!")

        # Add route for logout
        @app.route("/logout")
        def logout():
            resp = Html.make(redirect("/login"))
            resp.delete_cookie("authorization")
            return resp

        return cls

    @classmethod
    def verify_auth(cls):
        print("verify auth")
        auth = request.authorization
        if auth and auth.username == cls._username and auth.password == cls._password:
            print(auth.username, auth.password)
            return True
        elif request.cookies.get("authorization") == cls._authorization:
            return True
        return False

    @classmethod
    def required(cls, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if cls._enable:
                if cls.verify_auth() is False:
                    """Send login page or 401 response for basic auth"""
                    headers = {"WWW-Authenticate": 'Basic realm="nologin"'}
                    return response(
                        Rest.error("Login required!", status=401, headers=headers),
                        Html.make(redirect(f"/login?returnUrl={request.path}")),
                    )
            return f(*args, **kwargs)

        return decorated


def register_auth_handler(app):
    Auth.init_app(app)
